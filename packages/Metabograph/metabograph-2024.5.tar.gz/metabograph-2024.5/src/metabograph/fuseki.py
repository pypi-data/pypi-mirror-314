#!/usr/bin/env python3
"""Run the Fuseki server."""

import argparse
import logging
import os
import pathlib
import shlex
import subprocess
import sys
import tempfile

from .biopax.query_manager import BiopaxQueryManager
from .config import Config
from .exception import MetabographException, MetabographRuntimeError
from .logging import configure_logging


LOGGER = logging.getLogger(__name__)
# The environment variable with the path to the installed Fuseki directory.
FUSEKI_HOME_VAR = "FUSEKI_HOME"


def run_fuseki_server(config):
    """
    Context manager to launch a Fuseki server
    """
    bdm = BiopaxQueryManager(config)
    fuseki_home = os.getenv(FUSEKI_HOME_VAR)
    if fuseki_home is None:
        raise MetabographRuntimeError(
            f"The {FUSEKI_HOME_VAR} environment variable is not set."
        )
    fuseki_home = pathlib.Path(fuseki_home).resolve()

    with tempfile.TemporaryDirectory() as tmp_dir:
        owl_paths = bdm.get_owl_files(tmp_dir)
        file_args = (f"--file={p}" for p in owl_paths)
        cmd = [
            str(fuseki_home / "fuseki-server"),
            *file_args,
            "/",
        ]
        LOGGER.info("Starting Fuseki server: %s", " ".join(shlex.quote(w) for w in cmd))
        LOGGER.info("Press <ctrl>+c to exit.")
        try:
            subprocess.run(cmd, check=True, cwd=tmp_dir)
        except subprocess.CalledProcessError as err:
            raise MetabographRuntimeError(err) from err


def main(args=None):
    """
    Run the Fuseki server.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config", type=pathlib.Path, help="The Metabograph configuration file."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show debug messages."
    )
    pargs = parser.parse_args(args=args)
    configure_logging(level=logging.DEBUG if pargs.verbose else logging.INFO)
    config = Config(path=pargs.config)
    run_fuseki_server(config)


def run_main(args=None):
    """
    Wrapper around main with error handling.
    """
    try:
        main(args=args)
    except KeyboardInterrupt:
        pass
    except MetabographException as err:
        sys.exit(err)


if __name__ == "__main__":
    run_main()
