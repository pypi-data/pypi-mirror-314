#!/usr/bin/env python3
"""Map IDs between databases using UniProt's ID Mapping service."""

import argparse
import json
import logging
import os
import pathlib
import sys

from .cache import CacheManager
from .exception import UniprotIdMappingException
from .id_mapper import IdMapper


JSON_DUMP_ARGS = {"indent": 2, "sort_keys": True}


def parse_args(args=None):
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        help="""
            A directory for caching results locally. If not given, a standard
            path will be used.
        """,
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output results in JSON."
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        help="Timeout for establishing remote connections.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase logging level to DEBUG."
    )
    subparsers = parser.add_subparsers()

    map_parser = subparsers.add_parser(
        "map", help="Map given IDs from one database to another"
    )
    map_parser.add_argument("from", help="The database of the given IDs.")
    map_parser.add_argument(
        "to", help="The target database to which to map the given IDs."
    )
    map_parser.add_argument("id", nargs="*", help="The IDs to map.")
    map_parser.add_argument(
        "--id-list", help="Path to a file with a list of IDs, one per line."
    )
    map_parser.add_argument(
        "--refresh-missing",
        action="store_true",
        help="""
            Query the server for previously missing identifiers instead of using
            cached values.
        """,
    )
    map_parser.set_defaults(cmd="map")

    list_parser = subparsers.add_parser(
        "list", help='List available "from" and "to" databases.'
    )
    list_parser.set_defaults(cmd="list")

    clear_parser = subparsers.add_parser(
        "clear",
        help="""
            Clear the cache. If you only wish to clear missing identifiers, use
            the --clear-missing option of the "map" command.
        """,
    )
    clear_parser.set_defaults(cmd="clear")

    pargs = parser.parse_args(args=args)

    if getattr(pargs, "cmd", None) is None:
        parser.print_usage()
        sys.exit(os.EX_USAGE)

    return pargs


def _map(pargs, id_mapper):
    """
    Map the given IDs to the target database.

    Args:
        pargs:
            The parsed arguments.

        id_mapper:
            An IdMapper instance.
    """
    ids = set(i for i in pargs.id if i)
    if pargs.id_list:
        if pargs.id_list == "-":
            lines = sys.stdin
        else:
            lines = pathlib.Path(pargs.id_list).read_text(encoding="utf-8").splitlines()
        lines = (line.strip() for line in lines)
        lines = (line for line in lines if line)
        ids.update(lines)
    mapped = id_mapper.map_ids(
        getattr(pargs, "from"), pargs.to, ids, refresh_missing=pargs.refresh_missing
    )
    if pargs.json:
        print(json.dumps(mapped, **JSON_DUMP_ARGS))
        return
    for fro, to in sorted(mapped.items()):
        print(fro, to)


def main(pargs):
    """
    Main.

    Args:
        pargs:
            The parsed arguments.
    """
    cmd = pargs.cmd
    cache_man = CacheManager(cache_dir=pargs.cache_dir)

    if cmd == "clear":
        cache_man.clear()
        return

    id_mapper = IdMapper(cache_man=cache_man, timeout=pargs.timeout)
    if cmd == "list":
        froms = set()
        tos = set()
        for group in id_mapper.fields["groups"]:
            for item in group["items"]:
                if item.get("from", False):
                    froms.add(item["name"])
                if item.get("to", False):
                    tos.add(item["name"])
        froms = sorted(froms)
        tos = sorted(tos)
        if pargs.json:
            print(json.dumps({"from": froms, "to": tos}, **JSON_DUMP_ARGS))
        else:
            for title, items in (("From", froms), ("To", tos)):
                print(title)
                for item in items:
                    print(f"  {item}")
                print()
        return

    if cmd == "map":
        _map(pargs, id_mapper)
        return

    raise UniprotIdMappingException(f"Unrecognized command: {cmd}")


def run_main(args=None):
    """
    Wrapper around main with exception handling.
    """
    pargs = parse_args(args=args)
    logging.basicConfig(
        style="{",
        format="[{asctime}] {levelname} {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if pargs.verbose else logging.INFO,
    )
    try:
        main(pargs)
    except UniprotIdMappingException as err:
        sys.exit(err)


if __name__ == "__main__":
    run_main()
