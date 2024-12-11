#!/usr/bin/env python3
"""Utility functions."""


import hashlib
import logging
import os.path
import pathlib
from typing import Any

import pandas as pd


DEFAULT_HASH_ALGORITHM = "sha256"
LOGGER = logging.getLogger(__name__)


def dict_from_dataframe_columns(dataframe: pd.DataFrame, key_col: str, val_col: str):
    """
    Get a dict mapping key in one column of a dataframe to values in another
    column.

    Args:
        dataframe:
            The input dataframe.

        key_col:
            The name of the column with the keys.

        val_col:
            The name of the column with the corresponding values.

    Returns:
        A Python dict.
    """
    return dataframe[[key_col, val_col]].set_index(key_col).to_dict()[val_col]


def hash_data(data: Any, algorithm: str = DEFAULT_HASH_ALGORITHM):
    """
    Hash data.

    Args:
        data:
            The data to hash. If not a byte string then it will be converted to one.

        algorithm:
            The hashing algorithm to use.

    Returns:
        The hexdigest of the data and the algorithm used.
    """
    if not isinstance(data, bytes):
        if not isinstance(data, str):
            data = str(data)
        data = bytes(data, encoding="utf-8")
    return hashlib.new(algorithm, data).hexdigest(), algorithm


def hash_file(path: str | pathlib.Path, algorithm: str = DEFAULT_HASH_ALGORITHM):
    """
    Hash a file.

    Args:
        path:
            The path to the file.

        algorithm:
            The hashing algorithm to use.

    Returns:
        The hexdigest of the file and the algorithm used.
    """
    path = pathlib.Path(path).resolve()
    LOGGER.debug("Hashing %s with %s", path, algorithm)
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, algorithm).hexdigest(), algorithm


def is_older_or_missing(dst: str | pathlib.Path, src: str | pathlib.Path):
    """
    Check if the destination path is older than the source path or missing.

    Args:
        dst:
            The destination path.

        src:
            The source path.

    Returns:
        True if the destination path is older or missing, else False
    """
    dst = pathlib.Path(dst).resolve()
    src = pathlib.Path(src).resolve()
    try:
        LOGGER.debug("Stat'ing %s", dst)
        dst_mtime = dst.stat().st_mtime
    except FileNotFoundError:
        return True
    LOGGER.debug("Stat'ing %s", src)
    return dst_mtime < src.stat().st_mtime


def get_common_prefix(items):
    """
    Get the common prefix of an iterable of strings.

    Args:
        items:
            The items to parse.

    Returns:
        The common string prefix.
    """
    items = [str(i) for i in items]
    return os.path.commonprefix(items)
