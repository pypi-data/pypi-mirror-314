#!/usr/bin/env python3
"""
Run SPARQL queries on OWL files.
"""

import logging
import pathlib

import pandas as pd

try:
    import owlready2

    WorldType = owlready2.World
except ImportError:
    owlready2 = None
    WorldType = None  # pylint: disable=invalid-name

try:
    import rdflib
except ImportError:
    rdflib = None


from .exception import MetabographRuntimeError


LOGGER = logging.getLogger(__name__)


class OwlLoader:
    """
    Load OWL files and run SPARQL queries on them.
    """

    def __init__(self, cache_man, name, paths):
        """
        Args:
            cache_man:
                A CacheManager instance.

            name:
                A name for this loader. It will be used as a database name by
                the owlready backend to speed up queries after the initial
                loading.

            paths:
                Paths to OWL files to load.
        """
        self.cache_man = cache_man
        self.name = name
        self.paths = [pathlib.Path(p).resolve() for p in paths]
        self._owlready2_world = None
        self._rdflib_graph = None

    @property
    def owlready2_world(self) -> WorldType:
        """
        owlready2 ontology.
        """
        if not owlready2:
            return None
        if self._owlready2_world is None:
            db_path = self.cache_man.get_path(f"owlready/{self.name}.sqlite3")
            exists = db_path.exists()
            self._owlready2_world = owlready2.World(filename=db_path)
            if exists:
                LOGGER.info("Reloading cached data from %s", db_path)
            else:
                for path in self.paths:
                    LOGGER.info("Loading %s with owlready2", path)
                    self._owlready2_world.get_ontology(path.as_uri()).load()
                LOGGER.info("Caching data to %s", db_path)
                self._owlready2_world.save()
        return self._owlready2_world

    @property
    def rdflib_graph(self) -> rdflib.Graph:
        """
        Run a query using rdflib.
        """
        if not rdflib:
            return None
        if self._rdflib_graph is None:
            graph = rdflib.Graph()
            for path in self.paths:
                LOGGER.info("Loading %s with rdflib", path)
                graph.parse(str(path))
            self._rdflib_graph = graph
        return self._rdflib_graph

    def load(self):
        """
        Load the configured OWL files. Normally the OWL files are loaded lazily
        on demand but this function can be used to force loading of files from a
        temporary context.
        """
        if self.owlready2_world is None:
            if self.rdflib_graph is None:
                LOGGER.debug("Failed to load OWL files.")

    def query(self, query: str) -> pd.DataFrame:
        """
        Run a SPARQL query on the loaded ontology.

        Args:
            query:
                The SPARQL query to run.

        Returns:
            A Pandas dataframe with the results.
        """
        if not self.paths:
            return None

        graph = None
        world = self.owlready2_world
        if world:
            graph = world.as_rdflib_graph()
            backend = "owlready2"
        else:
            graph = self.rdflib_graph
            backend = "rdflib"
        if graph:
            LOGGER.debug("Running SPARQL query through %s", backend)
            rows = graph.query(query)
            LOGGER.debug("Converting query results to dataframe")
            return pd.DataFrame((row.asdict() for row in rows))

        raise MetabographRuntimeError(
            "One of the following packages is required: owlready2, rdflib"
        )
