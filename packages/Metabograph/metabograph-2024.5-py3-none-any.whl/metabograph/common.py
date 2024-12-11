#!/usr/bin/env python3
"""
Common global variables and functions.
"""

import datetime
import logging
import pathlib
import urllib.parse

import requests

from .exception import MetabographIOError

LOGGER = logging.getLogger(__name__)

# Internal name for cache directories and other uses.
NAME = "metabograph"

# HTTP header time format.
RFC_2616_FMT = "%a, %d %b %Y %H:%M:%S GMT"


def download(
    url: str,
    path: str | pathlib.Path,
    append_name: bool = False,
    timeout=10,
    force=False,
):
    """
    Download a URL to a path.

    Args:
        url:
            The URL to download.

        path:
            The output path.

        append_name:
            If True, append the URL's filename to the path.

        timeout:
            The timeout for remote requests, in seconds.

        force:
            By default, existing local files will only be overwritten if the
            remote server reports a newer modification time (or no modification
            time at all). Set this option to True to force a download without
            checking for remote modification times.

    Returns:
        The output path.
    """
    path = pathlib.Path(path).resolve()
    if append_name:
        path /= pathlib.Path(urllib.parse.urlparse(url).path).name
    if not force and path.exists():
        LOGGER.debug("Emitting HEAD request for %s", url)
        response = requests.head(url, timeout=timeout)
        try:
            remote_mtime = datetime.datetime.strptime(
                RFC_2616_FMT, response.headers["last-modified"]
            )
        except KeyError:
            pass
        else:
            local_mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
            if remote_mtime <= local_mtime:
                return path
    path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.info("Downloading %s to %s", url, path)
    with requests.get(url, stream=True, timeout=timeout) as stream:
        try:
            stream.raise_for_status()
            with path.open("wb") as handle:
                for chunk in stream.iter_content(chunk_size=8192):
                    handle.write(chunk)
        except IOError as err:
            raise MetabographIOError(err) from err
    return path
