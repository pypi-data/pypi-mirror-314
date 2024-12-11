#!/usr/bin/env python3
"""
Map IDs via the UniProt ID mapping service:
https://www.uniprot.org/help/id_mapping
"""

import functools
import logging
import sqlite3
import time

import requests

from .cache import CacheManager
from .exception import UniprotIdMappingException


LOGGER = logging.getLogger(__name__)


class IdMapperError(UniprotIdMappingException):
    """
    Custom exception raised by IdMapper.
    """


class IdMapper:
    """
    Wrapper around the UniProt ID mapping service with local caching.
    """

    EMPTY_PLACEHOLDER = ""

    def __init__(self, cache_man: CacheManager = None, timeout: float = 10):
        """
        Args:
            cache_man:
                A configured CacheManager instance.

            timeout:
                Connection timeout for remote requests, in seconds.
        """
        if cache_man is None:
            cache_man = CacheManager()
        self.cache_man = cache_man
        self.timeout = timeout
        self.conn = sqlite3.connect(self.local_database_path)

    @property
    def local_database_path(self):
        """The path to the cached database."""
        return self.cache_man.get_path("id_mapper.sqlite")

    @functools.cached_property
    def fields(self):
        """The available databases between which one can map IDs."""
        url = "https://rest.uniprot.org/configure/idmapping/fields"
        resp = requests.get(url, timeout=self.timeout)
        return resp.json()

    def _create_table_if_not_exists(self, table_name):
        """
        Create a table if it doesn't exist.

        Args:
            table_name:
                The name of the table.
        """
        with self.conn as cur:
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS "{table_name}"(col1 TEXT PRIMARY KEY, col2 TEXT)'
            )

    def _get_existing_entries(self, table_name, identifiers):
        """
        Get existing identifiers from the given table.

        Args:
            table_name:
                The name of the table to query.

            identifiers:
                The list of identifiers to query.

        Returns:
            A dict mapping found identifiers to their corresponding identifiers
            in the given table.

        """
        if not isinstance(identifiers, (str, tuple)):
            identifiers = list(identifiers)
        with self.conn as cur:
            placeholder = ",".join("?" for _ in identifiers)
            rows = cur.execute(
                f'SELECT col1, col2 FROM "{table_name}" WHERE col1 IN ({placeholder})',
                identifiers,
            )
            # Skip empty values which only serve as placeholders for remote
            # missing values.
            mapping = {k: None if v == self.EMPTY_PLACEHOLDER else v for (k, v) in rows}
            n_mapping = len(mapping)
            LOGGER.debug(
                "Retrieved %d cached value%s.", n_mapping, "" if n_mapping == 1 else "s"
            )
            return mapping

    def _insert_new_entries(self, table_name, rows):
        """
        Insert new entries into a table.

        Args:
            table_name:
                The name of the table.

            rows:
                An iterable of 2-tuples to insert into the table.
        """
        if rows:
            LOGGER.debug("Inserting %d rows into %s.", len(rows), table_name)
            with self.conn as cur:
                cur.executemany(
                    f'INSERT OR REPLACE INTO "{table_name}" VALUES (?, ?)', rows
                )

    def _clear_missing_values(self, table_name):
        """
        Clear missing values from a table so that they can be queried again on
        the server.

        Args:
            table_name:
                The table from which to clear missing values.
        """
        with self.conn as cur:
            cur.execute(
                f'DELETE FROM "{table_name}" WHERE "col2"=?', self.EMPTY_PLACEHOLDER
            )

    def _query_missing(self, db_from, db_to, identifiers):
        """
        Query the UniProt service for identifiers.

        Args:
            db_from:
                The database from which to map the identifiers.

            db_to:
                The database to which to map the identifiers.

            identifiers:
                The identifiers in db_from that should be mapped to db_to.

        Returns:
            A generator over lists of 2-tuples mapping the given identifiers to
            identifiers in db_to.

        Raises:
            IdMapperError:
                Failed to retrieve results from remote ID Mapping service.
        """
        i = 0
        while True:
            # Map number of IDs that can be submitted for one job.
            j = i + 100000
            batch = identifiers[i:j]
            i = j
            if not batch:
                break
            mapping_url = "https://rest.uniprot.org/idmapping"
            LOGGER.debug(
                "Submitting job to %s/run (%s -> %s) with %d identifiers.",
                mapping_url,
                db_from,
                db_to,
                len(batch),
            )
            resp = requests.post(
                f"{mapping_url}/run",
                data={"ids": ",".join(batch), "from": db_from, "to": db_to},
                timeout=self.timeout,
            )
            if resp.status_code != 200:
                for message in resp.json().get("messages"):
                    LOGGER.error("%s", message)
                raise IdMapperError("Failed to submit job.")
            try:
                job_id = resp.json()["jobId"]
            except KeyError as err:
                raise IdMapperError(
                    f"Response from {mapping_url} does not contain a job ID."
                ) from err
            poll_url = f"{mapping_url}/status/{job_id}"
            LOGGER.info("Waiting for job %s.", job_id)
            while True:
                LOGGER.debug("Polling %s.", poll_url)
                # Disable redirects to avoid retrieving the results here. We
                # want the stream URL below.
                resp = requests.get(
                    poll_url, timeout=self.timeout, allow_redirects=False
                )
                if resp.status_code not in (200, 303):
                    raise IdMapperError(
                        f"Failed to poll {poll_url} [status code: {resp.status_code}]: "
                        f"{resp.content}"
                    )
                result = resp.json()
                if result["jobStatus"] == "FINISHED":
                    LOGGER.info("Job %s is finished.", job_id)
                    break
                time.sleep(5)
            result_url = f"{mapping_url}/stream/{job_id}"
            LOGGER.debug("Retrieving results from %s.", result_url)
            yield [
                (r["from"], r["to"] if isinstance(r["to"], str) else r["to"]["id"])
                for r in requests.get(result_url, timeout=self.timeout).json()[
                    "results"
                ]
            ]

    @staticmethod
    def _get_table_name(db_from, db_to):
        """
        Get an SQLite3-safe table name for the given database names.

        Args:
            db_from:
                The database from which to map the identifiers.

            db_to:
                The database to which to map the identifiers.

        Returns:
            The table name, as a string.
        """
        return f"{db_from}___{db_to}"

    def map_ids(self, db_from, db_to, identifiers, refresh_missing=False):
        """
        Map identifiers from one database to another.

        Args:
            db_from:
                The database from which to map the identifiers.

            db_to:
                The database to which to map the identifiers.

            identifiers:
                The identifiers in db_from that should be mapped to db_to.

            refresh_missing:
                If True, check the server if previously missing values have been
                added since the last query.

        Returns:
            A dict mapping the found identifiers in db_from to identifiers in
            db_to.

        Raises:
            ValueError:
                Invalid arguments for db_from or db_to.
        """
        identifiers = set(str(i) for i in identifiers)
        if not identifiers:
            return {}
        if db_from == db_to:
            raise ValueError("db_from and db_to cannot be the same")
        table_name = self._get_table_name(db_from, db_to)
        self._create_table_if_not_exists(table_name)
        if refresh_missing:
            self._clear_missing_values(table_name)
        mapped = self._get_existing_entries(table_name, identifiers)
        missing = sorted(identifiers - set(mapped))
        if missing:
            for new_identifiers in self._query_missing(db_from, db_to, missing):
                self._insert_new_entries(table_name, new_identifiers)
                mapped.update(new_identifiers)
            still_missing = set(missing) - set(mapped)
            # Insert empty values to prevent redundant queries for remotely
            # missing values.
            if still_missing:
                n_still_missing = len(still_missing)
                LOGGER.debug(
                    "Inserting %d empty placeholder%s in %s.",
                    n_still_missing,
                    "" if n_still_missing == 1 else "s",
                    table_name,
                )
                self._insert_new_entries(
                    table_name, [(i, self.EMPTY_PLACEHOLDER) for i in still_missing]
                )
        # Clear the placeholder empty values.
        return {k: v for (k, v) in mapped.items() if v}
