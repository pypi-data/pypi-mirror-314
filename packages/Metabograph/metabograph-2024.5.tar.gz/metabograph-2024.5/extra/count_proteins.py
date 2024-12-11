#!/usr/bin/env python3
"""
Print information about protein entities. This information is used to verify
that all retrieved proteins are correctly identified.
"""

import logging
import os
import pathlib

import pandas as pd
from tabulate import tabulate

from metabograph.biopax.query_manager import BiopaxQueryManager
from metabograph.config import Config
from metabograph.logging import configure_logging


LOGGER = logging.getLogger(__name__)


def print_dataframe(data, max_rows=None, max_columns=None, width=None):
    """
    Print an unabbreviated dataframe.
    """
    with pd.option_context(
        "display.max_rows",
        max_rows,
        "display.max_columns",
        max_columns,
        "display.width",
        width,
        "display.max_colwidth",
        None,
    ):
        print(data)


def save_dataframe(data, path, **kwargs):
    """
    Save a dataframe to a file.
    """
    path = pathlib.Path(path).resolve()
    LOGGER.info("Saving data to %s", path)
    data.to_csv(path, **kwargs)


def chdir_and_get_config():
    """
    Change directory and get the Config instance.
    """
    project_dir = pathlib.Path(__file__).parent.parent
    tmp_dir = project_dir / "tmp/count_proteins"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(tmp_dir)
    config_path = project_dir / "config.yaml"
    return Config(config_path)


def main():
    """
    Main.
    """
    configure_logging(level=logging.DEBUG)
    config = chdir_and_get_config()

    bqm = BiopaxQueryManager(config, debug=True)
    #  bqm.cache_man.clear()
    prots = bqm.get_protein_entities()
    save_dataframe(prots, "proteins.csv", index=False)

    has_display_name = ~prots["display_names"].isna()
    has_uniprot_id = ~prots["uniprot"].isna()
    has_location = ~prots["location"].isna()
    has_xref = ~prots["xrefs"].isna()
    has_eref = ~prots["erefs"].isna()
    uniprot_in_eref_names = prots["eref_names"].str.contains("UniProt")
    has_member_uniprot = ~prots["member_uniprot"].isna()

    rows = [
        ("Number of rows in protein dataframe", prots.shape[0]),
        ("Unique protein entities", prots["entity"].nunique()),
        (
            "Unique protein entities with display names",
            prots[has_display_name]["entity"].nunique(),
        ),
        ("Unique display names", prots[has_display_name]["display_names"].nunique()),
        ("Unique UniProt IDs", prots[has_uniprot_id]["uniprot"].nunique()),
        ("Unique protein entities without cross-references", (~has_xref).sum()),
        ("Unique protein entities without reference entities", (~has_eref).sum()),
        (
            "Unique protein entities without display_name or reference entities",
            ((~has_display_name) & (~has_eref)).sum(),
        ),
        (
            "Entities with both a display name and a UniProt ID",
            prots[has_display_name & has_uniprot_id].shape[0],
        ),
        (
            "Entities with a display name and without a UniProt ID",
            prots[has_display_name & ~has_uniprot_id].shape[0],
        ),
        (
            "Entities without a display name and with a UniProt ID",
            prots[~has_display_name & has_uniprot_id].shape[0],
        ),
        (
            "Entities without a display name or a UniProt ID",
            prots[~has_display_name & ~has_uniprot_id].shape[0],
        ),
    ]
    rows.append(("Sum of last 4 rows", sum(item[1] for item in rows[-4:])))
    rows.extend(
        (
            (
                "Entities without a UniProt ID or any member UniProt IDs",
                prots[~has_uniprot_id & ~has_member_uniprot].shape[0],
            ),
            (
                'Entities without a UniProt ID but "UniProt" in entity reference names',
                prots[~has_uniprot_id & uniprot_in_eref_names].shape[0],
            ),
            (
                "Number of unique display names without a UniProt ID",
                prots[has_display_name & ~has_uniprot_id]["display_names"].nunique(),
            ),
            (
                "Number of unique UniProt IDs without a display name",
                prots[~has_display_name & has_uniprot_id]["uniprot"].nunique(),
            ),
            ("Entities with a location", has_location.sum()),
            ("Entities without a location", (~has_location).sum()),
        )
    )
    name_loc_keys = ["display_names", "location"]
    count_by_name_and_loc = (
        prots[has_display_name & has_location]
        .groupby(name_loc_keys)
        .count()
        .sort_values(name_loc_keys)
    )
    rows.extend(
        (
            (
                "Unique combinations of display name and location",
                count_by_name_and_loc.shape[0],
            ),
            (
                "Unique combinations of display name and location with single entity",
                count_by_name_and_loc[count_by_name_and_loc["entity"] == 1].shape[0],
            ),
            (
                "Unique combinations of display name and location with multiple entities",
                count_by_name_and_loc[count_by_name_and_loc["entity"] > 1].shape[0],
            ),
        )
    )
    rows.append(("Sum of last 2 rows", sum(item[1] for item in rows[-2:])))
    rows.extend(
        (
            (
                "Total number of entities grouped by display name and location",
                count_by_name_and_loc["entity"].sum(),
            ),
            (
                "Number of entities with unique combination of display name and location",
                count_by_name_and_loc[count_by_name_and_loc["entity"] == 1][
                    "entity"
                ].sum(),
            ),
            (
                "Number of entities that share a combination of display name and location",
                count_by_name_and_loc[count_by_name_and_loc["entity"] > 1][
                    "entity"
                ].sum(),
            ),
        )
    )
    rows.append(("Sum of last 2 rows", sum(item[1] for item in rows[-2:])))
    print(tabulate(rows, tablefmt="github", headers=["What", "Count"]))

    save_dataframe(
        count_by_name_and_loc["entity"],
        "display_name_and_loc_combination_counts.csv",
        index=True,
    )
    save_dataframe(
        count_by_name_and_loc[count_by_name_and_loc["entity"] > 1]["entity"],
        "non_unique_display_name_and_loc_combination_counts.csv",
        index=True,
    )
    orphans = prots[has_display_name & ~(has_uniprot_id | has_member_uniprot)][
        "display_names"
    ].sort_values()
    save_dataframe(orphans, "display_names_without_uniprot_id.csv", index=False)


if __name__ == "__main__":
    main()
