#!/usr/bin/env python3
"""
Cached data management.
"""

import logging
import pathlib
import shutil

import xdg.BaseDirectory

from .common import NAME
from .config import Config
from .exception import MetabographConfigError

LOGGER = logging.getLogger(__name__)


class CacheManager:
    """
    Manage cached data.
    """

    def __init__(self, config: Config):
        self.config = config

    @property
    def cache_dir(self) -> pathlib.Path:
        """
        The cache directory path.

        Returns:
            The path to this applications cache directory.
        """
        try:
            path = self.config.cache.path
            if not path:
                raise MetabographConfigError("Undefined cache path")
        except AttributeError:
            return pathlib.Path(xdg.BaseDirectory.xdg_cache_home).resolve() / NAME
        return self.config.resolve_path(path)

    def get_path(
        self, subpath: str | pathlib.Path, directory: bool = False
    ) -> pathlib.Path:
        """
        Get a path to a subpath in the cache directory. The parent directory
        will be created if missing.

        Args:
            subpath:
                A subpath to interpret relative to the cache directory.

            directory:
                If True, the subpath will be created as a directory.

        Returns:
            A path within the cache directory.
        """
        cache_dir = self.cache_dir
        path = cache_dir / subpath
        # Check that the subpath lies within the cache directory.
        if not path.is_relative_to(cache_dir):
            raise MetabographConfigError(
                f'The subpath "{subpath}" lies outside of the cache directory.'
            )
        # Create the required directories.
        (path if directory else path.parent).mkdir(parents=True, exist_ok=True)
        return path

    def clear(self):
        """
        Clear all cached data.
        """
        cache_dir = self.cache_dir
        LOGGER.info("Removing cache directory: %s", cache_dir)
        try:
            shutil.rmtree(cache_dir)
        except FileNotFoundError:
            pass
