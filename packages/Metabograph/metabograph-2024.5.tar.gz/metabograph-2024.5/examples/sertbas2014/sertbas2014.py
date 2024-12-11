#!/usr/bin/env python
"""
Example of BiopaxGraphGenerator subclass for custom BioPAX data.
"""

import logging
import pathlib
import urllib.request

import networkx

from metabograph.biopax.query_manager import BiopaxQueryManager
from metabograph.biopax.graph_generator import BiopaxGraphGenerator
from metabograph.config import Config
from metabograph.logging import configure_logging


THIS_PATH = pathlib.Path(__file__).resolve()
OWL_FILE_URL = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL1401240000/2/MODEL1401240000-biopax3.owl"
LOGGER = logging.getLogger(__name__)


class BGGSertbas2014(BiopaxGraphGenerator):
    """
    Custom subclass to force connections between reactions.
    """

    def get_node_identifier(self, node):
        """
        The same molecule maybe be produced or consumed in the same cellular
        location by different reactions. Because the input data labels each
        reactant and product of a reaction with the reaction's identifier, the
        equality of these entities is not recognized by the graph. This method
        corrects this.

        The generated identifier strips the reaction data from the identifier to
        ensure that reactions are connected via product-reactant nodes.
        """
        location = self.bqm.entity_to_location_name_mapper.get(node)
        location = f"{self.bqm.ITEM_DELIMITER}{location}" if location else ""
        try:
            name = node.rsplit("_m_", 1)[1]
        except IndexError:
            name = node.rsplit("_n_", 1)[1]
        return f"{name}{location}"

    def get_custom_node_attributes(self, node):
        """
        Add cell_type attribute based on identifier suffix ("_N" for neurons,
        "_A" for astrocytes).
        """
        if node.endswith("_N"):
            cell_type = "neuron"
        elif node.endswith("_A"):
            cell_type = "astrocyte"
        else:
            cell_type = "?"
        return {"cell_type": cell_type}


def download_data_if_missing(path):
    """
    Download BioPAX data to local OWL file.
    """
    if not path.exists():
        LOGGER.info("Downloading %s", OWL_FILE_URL)
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(OWL_FILE_URL) as hin, path.open("wb") as hout:
            while True:
                buf = hin.read(0x1000)
                if not buf:
                    break
                hout.write(buf)


def main():
    """
    Main.
    """
    configure_logging(level=logging.INFO)
    dir_path = THIS_PATH.parent
    config_path = dir_path / "config.yaml"
    config = Config(config_path)

    owl_path = config.resolve_path(config.biopax.custom_owl_files[0])
    download_data_if_missing(owl_path)

    bqm = BiopaxQueryManager(config, debug=False)
    #  bqm.cache_man.clear()
    bgg = BGGSertbas2014(bqm=bqm)

    graph = bgg.get_graph()
    LOGGER.info("Generated graph: %s", graph)

    graph_path = owl_path.parent / "graph.gml"
    LOGGER.info("Saving graph to %s", graph_path)
    networkx.write_gml(graph, str(graph_path))


if __name__ == "__main__":
    main()
