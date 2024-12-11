#!/usr/bin/env python3
"""
Download and query BioPAX data.

References:
* https://www.biopax.org/owldoc/Level3/
"""

import functools
import logging
import pathlib
import sys
import tempfile
import textwrap
import urllib.error
import zipfile
from typing import Any

import numpy as np
import pandas as pd
from SPARQLWrapper import SPARQLWrapper2

from ..cache import CacheManager
from ..common import download
from ..config import Config
from ..exception import MetabographIOError
from ..owl import OwlLoader
from ..sparql import COMMON_PREFIXES, hash_query
from ..utils import dict_from_dataframe_columns, is_older_or_missing, get_common_prefix
from .protein import get_protein_entities


LOGGER = logging.getLogger(__name__)


def _format_species(species: str) -> str:
    """
    Format a genus and species string for display.

    Args:
        species:
            The genus and species string, e.g. "homo sapiens".

    Returns:
        The formatted genus and species string, e.g. "Homo sapiens".
    """
    genus, species = species.replace("_", " ").split(None, 2)
    return f"{genus.title()} {species.lower()}"


def owl_file(species: str) -> str:
    """
    Get the name of the OWL file for the given species.
    """
    return f'{_format_species(species).replace(" ", "_")}.owl'


class BiopaxQueryManager:
    """
    BioPAX data manager.
    """

    ITEM_DELIMITER = ";;;"
    FIELD_DELIMITER = ":::"

    def __init__(self, config: Config, debug: bool = False):
        self.config = config
        self.debug = debug
        self.cache_man = CacheManager(self.config)
        self._owlloader = None
        self._sparqlwrapper = None
        self._constraints = None

    @property
    def biopax_dir(self) -> pathlib.Path:
        """
        The cache directory path for BioPAX data.
        """
        return self.cache_man.get_path("biopax", directory=True)

    @property
    def species(self) -> str:
        """
        The configured species.
        """
        return self.config.biopax.species

    @property
    def endpoint(self) -> str:
        """
        The configured SPARQL endpoint. It may be None.
        """
        return self.config.biopax.endpoint

    @property
    def level_3_owl_file(self) -> pathlib.Path:
        """
        Get the path to the BioPAX level 3 OWL file. This may be a
        user-configured path. It not set, the biopax.org data will be used. The
        file will be downloaded if necessary.
        """
        path = self.biopax_dir / "biopax-level3.owl"
        if not path.exists():
            url = "https://www.biopax.org/release/biopax-level3.owl"
            download(url, path)
        return path

    @property
    def reactome_archive_path(self) -> pathlib.Path:
        """
        The path to the zipped Reactome BioPAX archive with the specied data.
        The will will be downloaded if missing.
        """
        zip_path = self.biopax_dir / "biopax.zip"
        if not zip_path.exists():
            url = "https://reactome.org/download/current/biopax.zip"
            download(url, zip_path)
        return zip_path

    def extract_species_owl_file(self, dir_path: str | pathlib.Path) -> pathlib.Path:
        """
        Extract a species OWL file to a directory. The data will be downloaded
        if necessary.

        Args:
            dir_path:
                An output directory path.

        Returns:
            The path to the extract file.
        """
        dir_path = pathlib.Path(dir_path).resolve()
        dir_path.mkdir(parents=True, exist_ok=True)
        zip_path = self.reactome_archive_path
        species_file = owl_file(self.species)
        output_path = dir_path / species_file
        if is_older_or_missing(output_path, zip_path):
            LOGGER.info("Extracting %s from %s to %s", species_file, zip_path, dir_path)
            with zipfile.ZipFile(zip_path) as handle:
                handle.extract(species_file, path=dir_path)
        return output_path

    def get_owl_files(self, dir_path: str | pathlib.Path) -> list[pathlib.Path]:
        """
        Get the configured OWL files. Retrievable files may be downloaded or
        extracted to the given path. Existing files will simply return their
        paths, which may lie outside of the given directory.

        Args:
            dir_path:
                The path to a directory.

        Returns:
            The generator of OWL file paths as pathlib.Path objects.
        """
        # This file is necessary.
        yield self.level_3_owl_file
        bpconf = self.config.biopax
        if bpconf.include_default_owl_files:
            dir_path = pathlib.Path(dir_path).resolve()
            dir_path.mkdir(parents=True, exist_ok=True)
            yield self.extract_species_owl_file(dir_path)
        yield from bpconf.custom_owl_files

    def list_species(self) -> list[str]:
        """
        List the available species.
        """
        with zipfile.ZipFile(self.reactome_archive_path) as handle:
            for name in sorted(handle.namelist()):
                name = name.split(".", 1)[0]
                yield _format_species(name)

    def _query_sparqlwrapper(self, query: str) -> pd.DataFrame:
        """
        Query a SPARQL endpoint via SPARQLWrapper2.
        """
        endpoint = self.endpoint
        if self._sparqlwrapper is None:
            self._sparqlwrapper = SPARQLWrapper2(endpoint)
        self._sparqlwrapper.setQuery(query)
        try:
            LOGGER.debug("Sending SPARQL query to %s", endpoint)
            rows = self._sparqlwrapper.query().bindings
            LOGGER.debug("Converting query results to dataframe")
            return pd.DataFrame(
                [{key: value.value for (key, value) in row.items()} for row in rows]
            )
        except AttributeError:
            LOGGER.error("Query to %s failed: %s", endpoint, query)
            return None
        except urllib.error.URLError as err:
            LOGGER.error("Failed to query %s: %s", endpoint, err)
            raise MetabographIOError(err) from err

    def _query_owlloader(self, query: str) -> pd.DataFrame:
        """
        Query local OWL files.
        """
        if self._owlloader is None:
            with tempfile.TemporaryDirectory() as tmp_dir:
                paths = list(self.get_owl_files(tmp_dir))
                species_filename = pathlib.Path(owl_file(self.species)).stem.lower()
                name = f"biopax-{species_filename}"
                self._owlloader = OwlLoader(self.cache_man, name, paths)
                self._owlloader.load()
        return self._owlloader.query(query)

    @staticmethod
    def _custom_debug_msg(title: str, content: Any):
        """
        Print a custom debug message to STDERR.
        """
        width = 6
        content = str(content)
        for line in content.splitlines():
            width = max(width, len(line.rstrip()))
        line_chr = "-"
        # Ensure that even long titles are bookended by at least 3 line characters.
        header = f"{line_chr * 3}{title}{line_chr * 3}"
        header = str.center(title, width, line_chr)
        footer = line_chr * len(header)
        sys.stdout.write(f"{header}\n{content}\n{footer}\n")

    def _get_cached_query_path(self, query):
        """
        Get the path to a cached query depending on the query itself and the
        current configuration.

        Args:
            query:
                A SPARQL query string.
        """
        return (
            self.biopax_dir
            / "cached_queries"
            / self.species.replace(" ", "_")
            / f"{hash_query(query)}.csv"
        )

    def query(self, query: str) -> pd.DataFrame:
        """
        Run a SPARQL query on the loaded graph.

        Args:
            query:
                A SPARQL query string.
        """
        # Ensure that NaN and empty strings are preserved in the cached results.
        null_value = "NULL"
        query = textwrap.dedent(query).strip()
        query = f"{COMMON_PREFIXES}\n{query}"
        if self.debug:
            self._custom_debug_msg("SPARQL Query", query)
        path = self._get_cached_query_path(query)
        if path.exists():
            LOGGER.debug("Reloading cached query results from %s", path)
            try:
                data = pd.read_csv(path, na_values=[null_value], keep_default_na=False)
            except pd.errors.EmptyDataError:
                LOGGER.debug("Cached query data is empty: %s", path)
                return pd.DataFrame()
        else:
            if self.endpoint:
                data = self._query_sparqlwrapper(query)
            else:
                data = self._query_owlloader(query)
            # Convert empty fields to NaN.
            with pd.option_context("future.no_silent_downcasting", True):
                data.replace(r"^\s*$", np.nan, regex=True, inplace=True)
            LOGGER.debug("Caching query results to %s", path)
            path.parent.mkdir(parents=True, exist_ok=True)
            data.to_csv(path, index=False, na_rep=null_value)
        if self.debug:
            self._custom_debug_msg("SPARQL Query Results", data)
        return data

    def query_locations(self) -> pd.DataFrame:
        """
        Query all locations. Each entity is associated with at most one
        location.
        """
        query = """\
        SELECT DISTINCT ?entity ?location ?location_name
        WHERE {
            ?entity bp3:cellularLocation ?location.
            ?location bp3:term ?location_name.
        }
        """
        return self.query(query)

    def list_locations(self) -> list[str]:
        """
        List all known locations by name.
        """
        return sorted(self.query_locations()["location_name"].unique())

    def query_pathways(self) -> pd.DataFrame:
        """
        Query all pathways and their components.
        """
        query = """\
        SELECT DISTINCT ?pathway ?pathway_name ?component
        WHERE {
            ?pathway rdf:type bp3:Pathway;
                bp3:displayName ?pathway_name;
                bp3:pathwayComponent+ ?component.
        }
        """
        return self.query(query)

    def list_pathways(self) -> list[str]:
        """
        List all known pathways by name.
        """
        return sorted(set(self.query_pathways()["pathway_name"]))

    def query_entities(self) -> pd.DataFrame:
        """
        Query all entities and their types.
        """
        query = """\
        SELECT DISTINCT
            ?entity
            ?entity_type
        WHERE {
            ?entity rdf:type/rdfs:subClassOf* bp3:Entity;
                rdf:type ?entity_type.
        }
        """
        return self.query(query)

    def query_physical_entities(self) -> pd.DataFrame:
        """
        Query all physical entities and their references.
        """
        query = f"""\
        SELECT DISTINCT
            ?entity
            ?entity_type
            (GROUP_CONCAT(DISTINCT ?entity_name; separator="{self.ITEM_DELIMITER}") AS ?names)
            (
                GROUP_CONCAT(DISTINCT ?display_name; separator="{self.ITEM_DELIMITER}")
                AS ?display_names
            )
            (GROUP_CONCAT(DISTINCT ?eref; separator="{self.ITEM_DELIMITER}") AS ?erefs)
            (GROUP_CONCAT(DISTINCT ?eref_name; separator="{self.ITEM_DELIMITER}") AS ?eref_names)
            (GROUP_CONCAT(DISTINCT ?xref_str; separator="{self.ITEM_DELIMITER}") AS ?xrefs)
            (GROUP_CONCAT(DISTINCT ?member; separator="{self.ITEM_DELIMITER}") AS ?members)
        WHERE {{
            ?entity rdf:type/rdfs:subClassOf* bp3:PhysicalEntity;
                rdf:type ?entity_type.

            OPTIONAL {{
                ?entity bp3:name ?opt_entity_name.
            }}
            BIND(IF(BOUND(?opt_entity_name), ?opt_entity_name, "") AS ?entity_name)

            OPTIONAL {{
                ?entity bp3:displayName ?opt_display_name.
            }}
            BIND(IF(BOUND(?opt_display_name), ?opt_display_name, "") AS ?display_name)

            OPTIONAL {{
                ?entity bp3:entityReference+ ?opt_eref.
                ?opt_eref bp3:xref ?opt_xref;
                    bp3:name ?opt_eref_name.
                ?opt_xref bp3:id ?xref_id;
                    bp3:db ?xref_db.
                BIND(CONCAT(?xref_db,"{self.FIELD_DELIMITER}",?xref_id) AS ?opt_xref_str).
            }}
            BIND(IF(BOUND(?opt_eref), ?opt_eref, "") AS ?eref)
            BIND(IF(BOUND(?opt_eref_name), ?opt_eref_name, "") AS ?eref_name)
            BIND(IF(BOUND(?opt_xref_str), ?opt_xref_str, "") AS ?xref_str)

            OPTIONAL {{
                ?entity bp3:memberPhysicalEntity ?opt_member.
            }}
            BIND(IF(BOUND(?opt_member), ?opt_member, "") AS ?member)
        }}
        GROUP BY ?entity ?entity_type
        """
        return self.query(query)

    def query_interactions(self) -> pd.DataFrame:
        """
        Query all interactions.
        """
        query = """\
        SELECT DISTINCT ?interaction ?interaction_name
        WHERE {
            ?interaction rdf:type/rdfs:subClassOf* bp3:Interaction.

            OPTIONAL {
                ?interaction bp3:displayName ?opt_interaction_name.
            }
            BIND(IF(BOUND(?opt_interaction_name), ?opt_interaction_name, "") AS ?interaction_name)
        }
        """
        return self.query(query)

    def query_member_entities(self) -> pd.DataFrame:
        """
        Query all member entities.
        """
        query = """\
        SELECT DISTINCT ?a ?b
        WHERE {
            ?a bp3:memberPhysicalEntity ?b.
        }
        """
        return self.query(query)

    def query_conversion_directions(self) -> pd.DataFrame:
        """
        Query all conversion directions.
        """
        query = """\
        SELECT DISTINCT ?conversion ?direction
        WHERE {
            ?conversion rdf:type/rdfs:subClassOf* bp3:Conversion;
                bp3:conversionDirection ?direction.
        }
        """
        return self.query(query)

    def query_participants(self) -> pd.DataFrame:
        """
        Query all participant types.
        """
        query = """\
        SELECT DISTINCT ?participant
        WHERE {
            ?participant rdf:type/rdfs:subPropertyOf* bp3:participant.
        }
        """
        return self.query(query)

    def query_interaction_participants(self) -> pd.DataFrame:
        """
        Query all interaction-participant-entity relations.
        """
        query = """\
        SELECT DISTINCT ?interaction ?participant ?entity ?coefficient
        WHERE {
            ?interaction rdf:type/rdfs:subClassOf* bp3:Interaction.
            ?participant rdfs:subPropertyOf* bp3:participant.
            ?interaction ?participant ?entity.

            OPTIONAL {
                ?interaction bp3:participantStoichiometry ?opt_stoichiometry.
                ?opt_stoichiometry bp3:physicalEntity ?entity;
                    bp3:stoichiometricCoefficient ?opt_coeff.
            }
            BIND(IF(BOUND(?opt_coeff), ?opt_coeff, "") AS ?coefficient)
        }
        """
        return self.query(query)

    def query_controls(self) -> pd.DataFrame:
        """
        Query all controlled-controller relations.
        """
        query = """\
        SELECT DISTINCT ?controlled ?controller ?controlType
        WHERE {
            ?control rdf:type/rdfs:subClassOf* bp3:Control;
                bp3:controlled ?controlled;
                bp3:controller ?controller;
                bp3:controlType ?controlType.
        }
        """
        return self.query(query)

    def query_complex_components(self) -> pd.DataFrame:
        """
        Query all complex components.
        """
        query = """\
        SELECT DISTINCT ?complex ?component ?coefficient
        WHERE {
            ?complex rdf:type bp3:Complex.
            ?complex bp3:component ?component.

            OPTIONAL {
                ?complex bp3:componentStoichiometry ?opt_stoichiometry.
                ?opt_stoichiometry bp3:physicalEntity ?component;
                    bp3:stoichiometricCoefficient ?opt_coeff.
            }
            BIND(IF(BOUND(?opt_coeff), ?opt_coeff, "") AS ?coefficient)
        }
        """
        return self.query(query)

    def _map_key_to_values(
        self, data: pd.DataFrame, key_col: str, val_col: str
    ) -> pd.DataFrame:
        """
        Get a dict mapping keys to sets of values.

        Args:
            data:
                The dataframe from which to create the dict. It will be modified
                in-situ.

            key_col:
                The name of the key column.

            val_col:
                the name of the value column. The elements in this column are
                assumed to be separated by self.ITEM_DELIMITER.

        Returns:
            A dict mapping keys to sets of values.
        """
        mod_val_col = f"split_{val_col}"
        data[mod_val_col] = data[val_col].apply(
            lambda x: x.split(self.ITEM_DELIMITER) if isinstance(x, str) else pd.NA
        )
        return dict_from_dataframe_columns(data, key_col, mod_val_col)

    @functools.cached_property
    def entity_to_names_mappers(self) -> (dict[str, str], dict[str, str]):
        """
        Dicts mapping physical entities to names. The first maps entities to
        display names while the second maps entities to names. The names may be
        inconsistent due to the underlying data.

        TODO:
            Add support for other entity types.
        """
        physical_entities = self.query_physical_entities()
        data = pd.DataFrame(physical_entities[["entity", "display_names", "names"]])
        dnames = self._map_key_to_values(data, "entity", "display_names")
        names = self._map_key_to_values(data, "entity", "names")
        return dnames, names

    @functools.cached_property
    def entity_to_location_name_mapper(self) -> dict[str, str]:
        """
        A dict mapping entities to their locations.
        """
        locations = self.query_locations()
        return dict_from_dataframe_columns(locations, "entity", "location_name")

    @functools.cached_property
    def entity_to_type_mapper(self) -> dict[str, str]:
        """
        A dict mapping entities to their types.
        """
        entities = self.query_entities()
        key_col = "entity"
        val_col = "entity_type"
        data = pd.DataFrame(entities[[key_col, val_col]])
        data[val_col] = data[val_col].apply(lambda x: x.rsplit("#", 1)[1])
        return dict_from_dataframe_columns(data, key_col, val_col)

    @functools.cached_property
    def entity_to_simplified_id(self) -> dict[str, str]:
        """
        A dict mapping entities to simplified ID strings. This works by removing
        the common prefix from all entities. If there is no common prefix, the
        returned dict will be empty.
        """
        entities = self.query_entities()
        key_col = "entity"
        val_col = "simplified"
        data = pd.DataFrame(entities[key_col])
        prefix_len = len(get_common_prefix(data[key_col]))
        if prefix_len == 0:
            return {}
        data[val_col] = data[key_col].apply(lambda x: x[prefix_len:])
        return dict_from_dataframe_columns(data, key_col, val_col)


# Add methods define in other modules.
BiopaxQueryManager.get_protein_entities = get_protein_entities
