#!/usr/bin/env python3
"""Metabograph command-line application."""

import argparse
import logging
import pathlib
import sys
from collections.abc import Iterable
from typing import Any

import networkx

from .biopax.graph_generator import BiopaxGraphGenerator
from .biopax.query_manager import BiopaxQueryManager
from .config import Config
from .exception import MetabographException
from .logging import configure_logging

LOGGER = logging.getLogger(__name__)


def _print_list(title: str, items: Iterable[Any]):
    """
    Print a list.

    Args:
        title:
            The title of the list.

        items:
            The list items.
    """
    print(title)
    for item in items:
        print(f"  {item}")


def main(args=None):
    """
    Main function.
    """
    parser = argparse.ArgumentParser(
        description="Generate graphs from Reactome BioPAX data."
    )
    parser.add_argument(
        "config", nargs="?", help="Path to the YAML configuration file."
    )
    parser.add_argument(
        "graph", nargs="?", help="Output path for the generated graph in GML format."
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the cache to force a refresh of query data.",
    )
    parser.add_argument(
        "--create-config",
        type=pathlib.Path,
        metavar="PATH",
        help="""
            Create a YAML configuration file at the given path. If the path is
            "-", the generated YAML will be printed to STDOUT.
        """,
    )
    parser.add_argument(
        "--list-species", action="store_true", help="List available species."
    )
    parser.add_argument(
        "--list-locations",
        action="store_true",
        help="List recognized cellular locations.",
    )
    parser.add_argument(
        "--list-pathways", action="store_true", help="List recognized pathways."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increasing logging level to DEBUG. Pass twice to also show SPARQL queries.",
    )
    pargs = parser.parse_args(args=args)
    configure_logging(level=logging.DEBUG if pargs.verbose else logging.INFO)
    config = Config(path=pargs.config)
    bqm = BiopaxQueryManager(config, debug=pargs.verbose > 1)

    if pargs.clear_cache:
        bqm.cache_man.clear()

    if pargs.list_species:
        _print_list("Species", bqm.list_species())
        return

    if pargs.list_locations:
        _print_list("Cellular Locations", bqm.list_locations())
        return

    if pargs.list_pathways:
        _print_list("Pathways", bqm.list_pathways())
        return

    if pargs.create_config:
        config_text = config.get_documented_yaml()
        if pargs.create_config.name == "-":
            print(config_text)
            return
        path = pargs.create_config.resolve()
        LOGGER.info("Creating configuration file at %s", path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(config_text, encoding="utf-8")
        return

    LOGGER.info("Generating graph.")
    bgg = BiopaxGraphGenerator(bqm=bqm)
    graph = bgg.get_graph()

    if pargs.graph:
        path = pathlib.Path(pargs.graph).resolve()
        LOGGER.info("Saving graph to %s", path)
        path.parent.mkdir(parents=True, exist_ok=True)
        networkx.write_gml(graph, str(path))
        test = networkx.read_gml(str(path))
        print("Reloaded", test)
        return

    print("Generated graph:", graph)


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
