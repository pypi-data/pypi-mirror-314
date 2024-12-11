#!/usr/bin/env python3
"""Cache management."""

import logging
import pathlib
import shutil

from xdg.BaseDirectory import xdg_cache_home


LOGGER = logging.getLogger(__name__)


class CacheManager:
    """
    Cache manager.
    """

    NAME = __name__.split(".", 1)[0]

    def __init__(self, cache_dir=None):
        """
        Args:
            cache_dir:
                An optional path to a cache directory. If None, the standard XDG
                path will be used.
        """
        if cache_dir is not None:
            cache_dir = pathlib.Path(cache_dir).resolve()
        self._cache_dir = cache_dir

    @property
    def cache_dir(self):
        """
        The cache directory as a pathlib.Path object.
        """
        if self._cache_dir is not None:
            return self._cache_dir
        return pathlib.Path(xdg_cache_home).resolve() / self.NAME

    def get_path(self, subpath, is_dir=False):
        """
        Get the full path to a subdirectory of the cache directory.

        Args:
            subpath:
                The subpath within the cache directory.

            is_dir:
                If True, treat the subpath as a directory.

        Returns:
            The full path to the given subpath. The parent directory will be
            created if missing. If is_dir is True, so will the final path
            component.
        """
        path = self.cache_dir / subpath
        parent = path if is_dir else path.parent
        parent.mkdir(parents=True, exist_ok=True)
        return path

    def clear(self):
        """
        Remove the cache directory.
        """
        LOGGER.info("Removing %s", self.cache_dir)
        try:
            shutil.rmtree(self.cache_dir)
        except FileNotFoundError:
            pass
