#!/usr/bin/env python3
"""
UniProt ID mapping.
"""

import contextlib
import logging

from uniprot_id_mapping import IdMapper
from uniprot_id_mapping.exception import UniprotIdMappingException
from uniprot_id_mapping.cache import CacheManager as UIM_CacheManager

from ..cache import CacheManager
from ..exception import MetabographException


LOGGER = logging.getLogger(__name__)


class MetabographIdMapperError(MetabographException):
    """
    Custom exception raised by IdMapper.
    """


@contextlib.contextmanager
def id_mapper_context(cache_man: CacheManager):
    """
    Context manager to obtain an instance of uniprot_id_mapping.IdMapper
    configured to use Metabograph's cache directory. The context will convert
    UniprotIdMappingExceptions to MetabographIdMapperErrors

    Args:
        cache_man:
            A CacheManager instance.

    Returns:
        A configured instance of uniprot_id_mapping.IdMapper
    """
    try:
        uim_cache_man = UIM_CacheManager(
            cache_dir=cache_man.get_path("uniprot", directory=True)
        )
        id_mapper = IdMapper(uim_cache_man)
        yield id_mapper
    except UniprotIdMappingException as err:
        raise MetabographIdMapperError(err) from err
