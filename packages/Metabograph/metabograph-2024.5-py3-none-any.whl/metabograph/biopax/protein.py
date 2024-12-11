#!/usr/bin/env
"""
Protein-specific methods for .
"""

import itertools
import logging

import pandas as pd

from ..uniprot.id_mapping import id_mapper_context


LOGGER = logging.getLogger(__name__)


def get_uniprot_id(row, bqm):
    """
    Get the UniProt ID for a row if it exists.

    Args:
        row:
            The row from the dataframe of entities.

        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        The UniProt ID, or None.
    """
    xrefs = row["xrefs"]
    if not xrefs or pd.isna(xrefs):
        return None
    for xref in xrefs.split(bqm.ITEM_DELIMITER):
        name, value = xref.split(bqm.FIELD_DELIMITER)
        if "UniProt" in name:
            return value
    return None


def _map_members_to_uniprot_ids(row, bqm, uniprot_dict):
    """
    Application function for map_members_to_uniprot_ids.
    """
    members = row["members"]
    if not members or pd.isna(members):
        return None
    uniprot_ids = set()
    for member in members.split(bqm.ITEM_DELIMITER):
        uniprot_id = uniprot_dict.get(member)
        if uniprot_id and not pd.isna(uniprot_id):
            uniprot_ids.add(uniprot_id)
    if uniprot_ids:
        return bqm.ITEM_DELIMITER.join(sorted(uniprot_ids))
    return None


def map_members_to_uniprot_ids(prot_ents, bqm):
    """
    Get a series with UniProt IDs of the members in the members column.

    Args:
        prot_ents:
            The protein entity dataframe.

        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        A Pandas series with the UniProt IDs.
    """
    uniprot_dict = prot_ents.set_index("entity").to_dict()["uniprot"]
    return prot_ents.apply(
        _map_members_to_uniprot_ids, axis=1, args=(bqm, uniprot_dict)
    )


def _map_uniprot_ids_to_gene_id(value, bqm, id_map):
    """
    Application function for map_uniprot_ids_to_gene_ids.

    Args:
        value:
            The column value, containing 0 or more UniProt IDs separated by the
            bqm's item delimiter.

        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

        id_map:
            A dict mapping UniProt IDs to some gene ID.

    Returns:
        The mapped value.
    """
    if not value:
        return ""
    delimiter = bqm.ITEM_DELIMITER
    return delimiter.join(id_map.get(v, "") for v in value.split(delimiter))


def map_uniprot_ids_to_gene_ids(prot_ents, bqm):
    """
    Map UniProt IDs to different gene IDs (GeneID, Ensembl).

    Args:
        prot_ents:
            The protein entity dataframe.

        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        The input dataframe with additional columns for the gene IDs. They will
        follow the format of the UniProt ID columns. For example, The "uniprot"
        column will map to a "geneid" column, and the "member_uniprot" will map
        to a "member_geneid" column. Multiple UniProt IDs separated by the
        BiopaxQueryManager's item delimiter will map to multiple gene IDs
        separated by the same delimiter. Missing values will map to empty
        strings.
    """
    non_null_uniprot = ~prot_ents["uniprot"].isnull()
    non_null_member_uniprot = ~prot_ents["member_uniprot"].isnull()

    # Collect all of the UniProt IDs.
    uniprot_ids = set(prot_ents[non_null_uniprot]["uniprot"].unique())
    member_uniprot_ids = (
        prot_ents["member_uniprot"][non_null_member_uniprot]
        .apply(lambda x: x.split(bqm.ITEM_DELIMITER))
        .tolist()
    )
    uniprot_ids.update(itertools.chain.from_iterable(member_uniprot_ids))

    with id_mapper_context(bqm.cache_man) as id_mapper:
        for gene_id in ("GeneID", "Ensembl"):
            id_map = id_mapper.map_ids("UniProtKB_AC-ID", gene_id, uniprot_ids)
            for prefix in ("", "member_"):
                prot_ents[f"{prefix}{gene_id}".lower()] = prot_ents[
                    f"{prefix}uniprot"
                ].apply(_map_uniprot_ids_to_gene_id, args=(bqm, id_map))


def get_protein_entities(bqm):
    """
    Get the dataframe of protein entities.

    Args:
        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        A Pandas DataFrame.
    """
    phys_ents = bqm.query_physical_entities().merge(
        bqm.query_locations(), how="left", on="entity"
    )
    prot_ents = phys_ents[phys_ents["entity"].str.contains("Protein")].copy()
    if prot_ents.shape[0] != prot_ents["entity"].nunique():
        LOGGER.warning("Duplicate protein entities found in dataframe")

    no_display_name = prot_ents["display_names"].isna()
    if no_display_name.any():
        n_missing = no_display_name.sum()
        LOGGER.warning(
            "%d entit%s missing a display name",
            n_missing,
            "y is" if n_missing == 1 else "ies are",
        )
        no_other_name = prot_ents[no_display_name]["names"].isna()
        if no_other_name.any():
            n_missing = no_other_name.sum()
            LOGGER.warning(
                "%d entit%s have no name at all",
                n_missing,
                "y" if n_missing == 1 else "ies",
            )

    multiple_display_name = prot_ents["display_names"].str.contains(bqm.ITEM_DELIMITER)
    if multiple_display_name.any():
        n_multi = multiple_display_name.sum()
        LOGGER.warning(
            "%d entit%s have multiple display names",
            n_multi,
            "y" if n_multi == 1 else "ies",
        )

    prot_ents["uniprot"] = prot_ents.apply(get_uniprot_id, axis=1, args=(bqm,))
    prot_ents["member_uniprot"] = map_members_to_uniprot_ids(prot_ents, bqm)

    map_uniprot_ids_to_gene_ids(prot_ents, bqm)

    return prot_ents
