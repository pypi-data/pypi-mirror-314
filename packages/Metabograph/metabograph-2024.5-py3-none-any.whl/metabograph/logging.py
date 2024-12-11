#!/usr/bin/env python3
"""
Configure logging.
"""

import logging

LOGGER = logging.getLogger(__name__)


def configure_logging(level=logging.INFO):
    """
    Configure logging.

    Args:
        level:
            Logging level.
    """
    logging.basicConfig(
        style="{",
        format="[{asctime}] {levelname} {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )
