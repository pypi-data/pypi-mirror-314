#!/usr/bin/env python3
"""
Create NetworkX graphs from BioPAX data.
"""

import enum
import logging
from collections.abc import Iterable
from typing import Self, Any

import networkx as nx
import pandas as pd

from ..config import Config
from ..utils import dict_from_dataframe_columns
from .query_manager import BiopaxQueryManager


LOGGER = logging.getLogger(__name__)


@enum.unique
class Direction(enum.Enum):
    """
    Directions for some participant relations.
    """

    REVERSIBLE = enum.auto()
    LEFT_TO_RIGHT = enum.auto()
    RIGHT_TO_LEFT = enum.auto()

    def __str__(self) -> str:
        return self.name.replace("_", "-")

    @classmethod
    def from_str(cls, string: str) -> Self:
        """
        Convert a string to an instance of Direction.

        Args:
            string:
                The string to convert.

        Returns:
            The corresponding Direction.
        """
        if isinstance(string, cls):
            return string
        if not isinstance(string, str):
            string = str(string)
        return cls[string.upper().replace("-", "_")]


class BiopaxGraphGenerator:
    """
    Create NetworkX graphs from BioPAX data.
    """

    def __init__(self, *, config: Config = None, bqm: BiopaxQueryManager = None):
        """
        Args:
            config:
                An instance of Config. If not given, then the bqm parameter is
                required and the configuration from the BiopaxQueryManager
                instance will be used.

            bqm:
                An instance of BiopaxQueryManager. If not given, one will be
                instantiated from the given Config instance.
        """
        if bqm is None:
            bqm = BiopaxQueryManager(config)
        self.config = bqm.config
        self.bqm = bqm
        self._cached_data = {}

    def get_node_identifier(self, node: str) -> str:
        """
        Get a node identifier for the given node. This is sometimes required to
        ensure that the same entity is recognized as such when input data
        assigns different identifiers to the same entity. Subclass this class
        and override this method to handle custom identifiers.

        Args:
            node:
                The node identifier, usually the entity string.

        Returns:
            The possibly modified node identifier to use for nodes in the graph.
        """
        return node

    def get_custom_node_attributes(self, node: str) -> dict[str, Any]:
        """
        Get custom node attributes. Override in a subclass for custom user data.

        Args:
            node:
                The target node.

        Returns:
            A dict of custom node attributes to add to the given node.
        """
        return {}

    @staticmethod
    def _log_graph_addition(number: int, singular: str, plural: str = None):
        """
        Internal function for logging additions to the graph.

        Args:
            number:
                The number of elements added.

            singular:
                The display name for one element.

            plural:
                The display name for more than one element. If None, an "s" will
                be added to the singular name.
        """
        if plural is None:
            plural = f"{singular}s"
        LOGGER.info(
            "Adding %d %s to graph", number, singular if number == 1 else plural
        )

    def _add_and_log_graph_edges(
        self, graph: nx.Graph, edges: pd.Series, *args: str, **kwargs: str
    ):
        """
        Add edges to the graph and log how many where added.

        Args:
            graph:
                The nx.Graph object.

            edges:
                A Pandas series of edges to add via the nx.Graph.add_edges_from
                method.

            *args:
                Keyword arguments that will be passed through to
                _log_graph_addition after the number argument.

            **kwargs:
                Keyword arguments passed through to _log_graph_addition.
        """
        if edges.shape[0] > 0:
            self._log_graph_addition(edges.shape[0], *args, **kwargs)
            edges = edges.apply(
                lambda x: (
                    self.get_node_identifier(x[0]),
                    self.get_node_identifier(x[1]),
                    x[2],
                )
            )
            graph.add_edges_from(edges)

    @staticmethod
    def _keep_any_isin(
        data: pd.DataFrame, cols: list[str], items: Iterable[str]
    ) -> pd.DataFrame:
        """
        Keep rows for which at least one of the given columns contains a value
        in the given list of items.

        Args:
            data:
                The Dataframe to filter.

            cols:
                The list of column names to check.

            items:
                The iterable of values to check.

        Returns:
            The filtered dataframe.
        """
        if not isinstance(items, set):
            items = set(items)
        keep = None
        for col in cols:
            if keep is None:
                keep = data[col].isin(items)
            else:
                keep |= data[col].isin(items)
        return data[keep]

    @property
    def location_data(self):
        """
        The dataframe of location data.
        """
        key = "location_data"
        if self._cached_data[key] is None:
            self._cached_data[key] = self.bqm.query_locations()
        return self._cached_data[key]

    def filter_by_location(
        self, data: pd.DataFrame, ent_cols: list[str]
    ) -> pd.DataFrame:
        """
        Filter entities by their location.

        Args:
            data:
                The dataframe to filter.

            end_cols:
                The column names of the entities.

        Returns:
            The filtered dataframe.
        """
        # All entities are assocated with locations.
        locations = self.config.biopax.locations
        if locations:
            LOGGER.info("Filtering nodes by locations: %s", ", ".join(locations))
            loc_data = self.location_data
            known_loc = set(loc_data["entity"])
            selected_by_loc = set(
                loc_data[loc_data["location_name"].isin(locations)]["entity"]
            )
            keep = selected_by_loc
            if self.config.biopax.keep_unknown:
                keep |= set(data[ent_cols].values) - known_loc
            data = self._keep_any_isin(data, ent_cols, keep)
        return data

    @property
    def pathway_data(self):
        """
        The dataframe of pathway data.
        """
        key = "pathway_data"
        if self._cached_data[key] is None:
            self._cached_data[key] = self.bqm.query_pathways()
        return self._cached_data[key]

    def filter_by_pathway(
        self, data: pd.DataFrame, pathway_cols: list[str]
    ) -> pd.DataFrame:
        """
        Filter interactions by pathway.

        Args:
            data:
                The dataframe to filter.

            end_cols:
                The column names of the entities.

        Returns:
            The filtered dataframe.
        """
        # Only interactions are associated with pathways.
        pathways = self.config.biopax.pathways
        if pathways:
            LOGGER.info("Filtering interactions by pathways: %s", ", ".join(pathways))
            pathway_data = self.bqm.query_pathways()
            known_pathway_comps = set(pathway_data["component"])
            # Selected by pathway.
            keep = set(
                pathway_data[pathway_data["pathway_name"].isin(pathways)]["component"]
            )
            if self.config.biopax.keep_unknown:
                keep |= set(data[pathway_cols]) - known_pathway_comps
            data = self._keep_any_isin(data, pathway_cols, keep)

        return data

    def filter_controls(
        self, controls: pd.DataFrame, interaction_participants: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Filter controlled-controller relations to those for which the controlled
        entity is included in the interaction participants.

        Args:
            controls:
                The controls dataframe.

            interaction_participants:
                The interaction participants dataframe.
        """
        keep = controls["controlled"].isin(interaction_participants["interaction"])
        return controls[keep]

    def filter_complexes(
        self, complex_components: pd.DataFrame, interaction_participants: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Filter complex components to those containing the selected interaction
        participants. All components of each complex containing an interaction
        participant entity will be kept. This is used to indirectly filter by
        pathways.


        Args:
            complex_components:
                The complex components dataframe.

            interaction_participants:
                The interaction participants dataframe.
        """
        component_to_complex = dict_from_dataframe_columns(
            complex_components, "component", "complex"
        )
        complexes = (
            interaction_participants["entity"]
            .apply(lambda x: component_to_complex.get(x, pd.NA))
            .dropna()
        )
        complexes = pd.concat([complexes, interaction_participants["entity"]]).unique()
        keep = complex_components["complex"].isin(complexes)
        return complex_components[keep]

    def filter_member_entities(
        self, member_entities: pd.DataFrame, interaction_participants: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Filter member_entities to those containing the selected interaction
        participants. All members with a transitive member relation to one of
        the interaction participants will be keps. This is used to indirectly
        filter by pathways.

        Args:
            member_entities:
                The member entities dataframe.

            interaction_participants:
                The interaction participants dataframe.
        """
        unsorted = member_entities["a"] > member_entities["b"]
        member_entities[["a", "b"]][unsorted] = member_entities[unsorted][["b", "a"]]
        member_entities = member_entities.sort_values(by=["a", "b"])
        # Partition the member entities into sets based on the transitive
        # relation. The previous sorting guarantees that previous members will
        # be found.
        member_sets = []
        for row in member_entities.itertuples():
            ent_a = row.a
            ent_b = row.b
            for mset in member_sets:
                if ent_a in mset:
                    mset.add(ent_b)
                    break
                if ent_b in mset:
                    mset.add(ent_a)
                    break
            else:
                member_sets.append(set((ent_a, ent_b)))
        keepers = set()
        for mset in member_sets:
            if interaction_participants["entity"].isin(mset).any():
                keepers.update(mset)
        # Only one column needs to be checked because of the transitive relation.
        keep = member_entities["a"].isin(keepers)
        return member_entities[keep]

    def get_graph(self) -> nx.Graph:
        """
        Get the graph for the current configuration.
        """
        graph = nx.DiGraph()
        node_set = set()
        edge_ops = []

        # All entities have a location so they can be filter by it directly.
        # Pathways are more complicated because only interactions are associated
        # directly with them. To filter other entities by pathway, we first
        # filter all of the interaction participants by their associated
        # interaction. Other entities such as controlers, complexes and member
        # entities are then filtered by the interations and physical entities
        # remaining in interaction_participants after these filters have been
        # applied.
        interaction_participants = self.bqm.query_interaction_participants()
        interaction_participants = self.filter_by_location(
            interaction_participants, ["interaction", "entity"]
        )
        interaction_participants = self.filter_by_pathway(
            interaction_participants, ["interaction"]
        )
        node_set.update(interaction_participants["interaction"])
        node_set.update(interaction_participants["entity"])
        edge_ops.append((self._add_participant_edges, interaction_participants))

        controls = self.bqm.query_controls()
        if not controls.empty:
            controls = self.filter_by_location(controls, ["controlled", "controller"])
            # Indirect pathways filtering.
            controls = self.filter_controls(controls, interaction_participants)
            #  The tiler ensures that "controlled" is already included.
            node_set.update(controls["controller"])
            edge_ops.append((self._add_control_edges, controls))

        if self.config.biopax.include_complexes:
            complex_components = self.bqm.query_complex_components()
            if not complex_components.empty:
                complex_components = self.filter_by_location(
                    complex_components, ["complex", "component"]
                )
                # Indirect pathway filtering.
                complex_components = self.filter_complexes(
                    complex_components, interaction_participants
                )
                node_set.update(complex_components["complex"])
                node_set.update(complex_components["component"])
                edge_ops.append((self._add_complex_component_edges, complex_components))

        if self.config.biopax.include_member_entities:
            member_entities = self.bqm.query_member_entities()
            if not member_entities.empty:
                member_entities = self.filter_by_location(member_entities, ["a", "b"])
                # Indirect pathway filtering.
                member_entities = self.filter_member_entities(
                    member_entities, interaction_participants
                )
                node_set.update(member_entities["a"])
                node_set.update(member_entities["b"])
                edge_ops.append((self._add_member_entity_edges, member_entities))

        self._add_nodes(graph, node_set)
        for edge_op in edge_ops:
            edge_op[0](graph, *edge_op[1:])
        return graph

    def _add_nodes(self, graph: nx.Graph, nodes: set[str]):
        """
        Add nodes to the graph.

        Args:
            graph:
                The graph instance.

            nodes:
                The set of entities to add.
        """
        entity_to_display_names, entity_to_names = self.bqm.entity_to_names_mappers
        entity_to_location = self.bqm.entity_to_location_name_mapper
        entity_to_type = self.bqm.entity_to_type_mapper
        entity_to_simplified = self.bqm.entity_to_simplified_id
        self._log_graph_addition(len(nodes), "node")
        for node in nodes:
            dnames = entity_to_display_names.get(node)
            dnames = (
                ";".join(dnames) if dnames else entity_to_simplified.get(node, node)
            )
            names = entity_to_names.get(node)
            names = ";".join(names) if names else ""
            attrs = {
                "type": entity_to_type[node],
                "display_names": dnames,
                "names": names,
                "location": entity_to_location.get(node, "?"),
            }
            attrs.update(self.get_custom_node_attributes(node))
            graph.add_node(self.get_node_identifier(node), **attrs)

    def _add_participant_edges(
        self, graph: nx.Graph, interaction_participants: pd.DataFrame
    ):
        """
        Get the participant edge from a row of the interaction participants
        dataframe.

        Args:
            graph:
                The graph instance.

            interaction_participants:
                The dataframe of participant relations between interactions and
                entities.
        """
        edge_data = pd.DataFrame()
        edge_data["node_1"] = interaction_participants["interaction"]
        edge_data["node_2"] = interaction_participants["entity"]
        edge_data["part_name"] = interaction_participants["participant"].apply(
            lambda x: str(x).rsplit("#", 1)[1].lower()
        )
        edge_data["coefficient"] = interaction_participants["coefficient"].astype(str)

        # The participant relations "left" and "right" can be used for reactions
        # that run left-to-right, right-to-left or both (reversible). The edge
        # directions must consider all cases even if the current version of
        # Reactome only contains interactions that run left-to-right.
        left_or_right = (edge_data["part_name"] == "left") | (
            edge_data["part_name"] == "right"
        )
        # The conversion directions can be LEFT-TO-RIGHT, RIGHT-TO-LEFT, or REVERSIBLE.
        conv_dirs = self.bqm.query_conversion_directions()
        # Map each conversion to its direction.
        if conv_dirs.empty:
            conv_dict = {}
        else:
            conv_dict = pd.Series(
                conv_dirs["direction"].values, index=conv_dirs["conversion"]
            ).to_dict()
        directed = interaction_participants[left_or_right]
        edge_data.loc[left_or_right, "direction"] = directed.apply(
            (
                lambda x: Direction.from_str(
                    conv_dict.get(x["interaction"], Direction.LEFT_TO_RIGHT)
                )
            ),
            axis=1,
        )
        self._add_left_and_right_edges(graph, edge_data[left_or_right])

        # Consider other edges as bidirectional.
        others = edge_data[~left_or_right]
        self._add_and_log_graph_edges(
            graph,
            others.apply(
                (
                    lambda x: (
                        x["node_1"],
                        x["node_2"],
                        {"type": x["part_name"], "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "bidirectional left edge",
        )
        self._add_and_log_graph_edges(
            graph,
            others.apply(
                (
                    lambda x: (
                        x["node_2"],
                        x["node_1"],
                        {"type": x["part_name"], "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "bidirectional right edge",
        )

    def _add_left_and_right_edges(self, graph: nx.Graph, directed: pd.DataFrame):
        """
        Add directed edges for the left and right participant relations.

        Args:
            graph:
                The graph instance.

            directed:
                The extract of the participant dataframe with "left" or "right"
                participant relations.
        """
        rev = directed["direction"] == Direction.REVERSIBLE
        l_to_r = (directed["direction"] == Direction.LEFT_TO_RIGHT) | rev
        r_to_l = (directed["direction"] == Direction.RIGHT_TO_LEFT) | rev
        left = directed["part_name"] == "left"
        right = directed["part_name"] == "right"

        # For left-to-right and reversible interactions, add edges
        # node_1 -left-> interaction -right-> node_2.
        self._add_and_log_graph_edges(
            graph,
            directed[l_to_r & left].apply(
                (
                    lambda x: (
                        x["node_2"],
                        x["node_1"],
                        {"type": "left", "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "left-to-right left edge",
        )
        self._add_and_log_graph_edges(
            graph,
            directed[l_to_r & right].apply(
                (
                    lambda x: (
                        x["node_1"],
                        x["node_2"],
                        {"type": "right", "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "left-to-right right edge",
        )

        # For right-to-left and reversible interactions, add edges
        # node_1 <-left- interaction <-right- node_2.
        self._add_and_log_graph_edges(
            graph,
            directed[r_to_l & right].apply(
                (
                    lambda x: (
                        x["node_2"],
                        x["node_1"],
                        {"type": "right", "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "right-to-left right edge",
        )
        self._add_and_log_graph_edges(
            graph,
            directed[r_to_l & left].apply(
                (
                    lambda x: (
                        x["node_1"],
                        x["node_2"],
                        {"type": "left", "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "right-to-left left edge",
        )

    def _add_control_edges(self, graph: nx.Graph, controls: pd.DataFrame):
        """
        Add control edges.

        Args:
            graph:
                The graph instance.

            controls:
                The dataframe of control relationships.
        """
        edge_data = pd.DataFrame()
        edge_data["node_1"] = controls["controller"]
        edge_data["node_2"] = controls["controlled"]
        edge_data["type"] = controls["controlType"]
        self._add_and_log_graph_edges(
            graph,
            edge_data.apply(
                (
                    lambda x: (
                        x["node_1"],
                        x["node_2"],
                        {"type": f"control:{x['type']}"},
                    )
                ),
                axis=1,
            ),
            "control edge",
        )

    def _add_complex_component_edges(
        self, graph: nx.Graph, complex_components: pd.DataFrame
    ):
        """
        Add component edges for complexes.

        Args:
            graph:
                The graph instance.

            complex_components:
                The dataframe with complex component relations.
        """
        edge_data = pd.DataFrame()
        edge_data["node_1"] = complex_components["complex"]
        edge_data["node_2"] = complex_components["component"]
        edge_data["coefficient"] = complex_components["coefficient"].astype(str)
        self._add_and_log_graph_edges(
            graph,
            edge_data.apply(
                (
                    lambda x: (
                        x["node_1"],
                        x["node_2"],
                        {"type": "complex:component", "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "complex to component edge",
        )
        self._add_and_log_graph_edges(
            graph,
            edge_data.apply(
                (
                    lambda x: (
                        x["node_2"],
                        x["node_1"],
                        {"type": "component:complex", "coefficient": x["coefficient"]},
                    )
                ),
                axis=1,
            ),
            "component to complex edge",
        )

    def _add_member_entity_edges(self, graph: nx.Graph, member_entities: pd.DataFrame):
        """
        Add member entity edges.

        Args:
            graph:
                The graph instance.

            member_entities:
                The dataframe of member entity relationships.
        """
        edge_data = pd.DataFrame()
        edge_data["node_1"] = member_entities["a"]
        edge_data["node_2"] = member_entities["b"]
        self._add_and_log_graph_edges(
            graph,
            edge_data.apply(
                (lambda x: (x["node_1"], x["node_2"], {"type": "member"})), axis=1
            ),
            "member entity edge",
        )
        self._add_and_log_graph_edges(
            graph,
            edge_data.apply(
                (lambda x: (x["node_2"], x["node_1"], {"type": "member"})), axis=1
            ),
            "member edge",
        )
