#!/usr/bin/env python3
"""
SPARQL query functions.
"""

import hashlib
import logging

from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.algebra import translateAlgebra

LOGGER = logging.getLogger(__name__)

# Common SPARQL prefixes.
COMMON_PREFIXES = """
PREFIX bio: <http://purl.org/vocab/bio/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bp3: <http://www.biopax.org/release/biopax-level3.owl#>
PREFIX reactome: <http://identifiers.org/reactome/>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX pubchem: <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/>
PREFIX fn: <http://www.w3.org/2005/xpath-functions#>
""".lstrip()


def canonicalize(query):
    """
    Canonicalize a SPARQL query. This uses rdflib's SPARQL parsing and algebra
    translation functions. The returned query string may be longer than the
    input string so this function should not be used to shorten queryies.

    Args:
        query:
            The input SPARQL query string.

    Returns:
        The canonicalized query string.
    """
    return translateAlgebra(prepareQuery(query))


def hash_query(query):
    """
    Get a hash value for a SPARQL query. This is used to cache query results.

    Args:
        query:
            The input query.

    Returns:
        A hash string.
    """
    query = canonicalize(query).encode("utf-8")
    hsh = hashlib.sha256()
    hsh.update(query)
    return hsh.hexdigest()
