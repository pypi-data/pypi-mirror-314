#!/usr/bin/env python3
"""
Graph configuration.
"""

import dataclasses
import logging
import pathlib
from typing import Any, Optional

from dataclass_documenter import DataclassDocumenter

import yaml


LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class CacheData:
    """
    Cache data configuration.

    Parameters:
        path:
            The path to a cache directory. If unset, the standard XDG user cache
            directory will be used.

        timeout:
            The timeout for the cached data. Data will be cleared from the cache
            after this timeout. If unset, cached data will not automatically
            time out.
    """

    path: Optional[pathlib.Path] = None
    timeout: Optional[int] = None


@dataclasses.dataclass
class BiopaxData:  # pylint: disable=too-many-instance-attributes
    """
    BioPAX data configuration.

    Parameters:
        endpoint:
            An optional URL to a SPARQL endpoint through which to query BioPAX
            data, such as a local Fuseki server.

        include_default_owl_files:
            If True, include the default BioPAX files for the configured
            species. These files will be downloaded if necessary.

        custom_owl_files:
            A list of paths to custom OWL files in the BioPAX level-3 format to
            use, either with or without the default files depending on the value
            of include_default_owl_files.

        include_complexes:
            If True, include complexes and their components.

        include_member_entities:
            If True, include member entities (as defined by BioPAX).

        keep_unknown:
            If True, items for which a pathway or location is unknown will be
            kept when filtering by pathway and/or location.

        locations:
            Either a list of BioPax entity locations, or a path to a plaintext
            file with one location per line. See `metabograph --list-locations`
            for the complete list.

        pathways:
            Either a list of BioPAX pathways, or a path to a plaintext file with
            one pathways per line. See `metabograph --list-pathways` for the
            complete list.

        species:
            The target species. It must be one supported by BioPAX. See
            `metabograph --list-species` for the complete list.
    """

    custom_owl_files: list[pathlib.Path] = dataclasses.field(default_factory=list)
    endpoint: Optional[str] = None
    include_complexes: bool = True
    include_default_owl_files: bool = True
    include_member_entities: bool = False
    keep_unknown: bool = False
    locations: Optional[list[str] | str] = None
    pathways: Optional[list[str] | str] = None
    species: str = "homo sapiens"

    def __post_init__(self):
        self.custom_owl_files = [pathlib.Path(p) for p in self.custom_owl_files]

        for field in ("locations", "pathways"):
            value = getattr(self, field)
            if isinstance(value, str):
                LOGGER.info("Loading %s from %s", field, value)
                path = pathlib.Path(value)
                values = set(path.read_text(encoding="utf-8").splitlines())
                values = sorted(val for val in values if val)
                setattr(self, field, values)


@dataclasses.dataclass
class ConfigData:
    """
    Main configuration.

    Parameters:
        cache:
            Cache configuration.

        biopax:
            BioPAX configuration.
    """

    biopax: BiopaxData = dataclasses.field(default_factory=BiopaxData)
    cache: CacheData = dataclasses.field(default_factory=CacheData)

    def __post_init__(self):
        if isinstance(self.cache, dict):
            self.cache = CacheData(**self.cache)  # pylint: disable=not-a-mapping

        if isinstance(self.biopax, dict):
            self.biopax = BiopaxData(**self.biopax)  # pylint: disable=not-a-mapping


class Config:
    """
    Graph configuration.
    """

    def __init__(self, path: str | pathlib.Path = None, data: dict = None):
        """
        Args:
            path:
                The path to a YAML configuration file that should be loaded.

            data:
                A dict of keyword parameters for instantiating an instance of
                ConfigData.
        """
        if data is None:
            data = {}
        self.__dict__["data"] = ConfigData(**data)

        self.__dict__["path"] = None
        if path is not None:
            self.load(path)

    def load(self, path: str | pathlib.Path):
        """
        Load a configuration file.
        """
        self.__dict__["path"] = pathlib.Path(path).resolve()
        with self.path.open("rb") as handle:
            self.data = ConfigData(**yaml.safe_load(handle))

    def resolve_path(self, path: str | pathlib.Path) -> pathlib.Path:
        """
        Resolve a path relative to the configuration file's path if the path is
        set.

        Args:
            path:
                The path to resolve.

        Returns:
            The resolved path.
        """
        if self.path:
            return self.path.parent.joinpath(path)
        return pathlib.Path(path).resolve()

    def asdict(self):
        """
        Return the dict representing the current ConfigData object.
        """
        return dataclasses.asdict(self.data)

    def __getattr__(self, key: str) -> Any:
        try:
            return self.__dict__[key]
        except KeyError:
            return getattr(self.data, key)

    def __setattr__(self, key: str, value: Any):
        if key == "data":
            self.__dict__[key] = value
        else:
            setattr(self.data, key, value)

    def get_documented_yaml(self):
        """
        Return the current object as a commented YAML document.
        """
        return DataclassDocumenter(ConfigData).get_yaml()
