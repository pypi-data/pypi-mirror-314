# TODO

## Bugs

* Debug node and edge attributes. The error may be due to bidirectional edges: https://stackoverflow.com/questions/26691442/how-do-i-add-a-new-attribute-to-an-edge-in-networkx

## General

* Add command-line tool with options to show and/or insert constraints into configuration file.
* Add cache validation check method.

## BioPAX

* `bindsTo` and `BindingFeature`?
* `Control`, `Conversion`, `GeneticInteraction`, `MolecularInteraction`, `TemplateReaction`
* Use `conversionDirection` to qualify all conversion reactions.
* Add complex components to graph.

## Graph

* Reconsider type attribute for symmetric bidirectional edges.
* Add functions to generate NetworkX graphs of the 3 types suggested by Nicolas (entity notes, interaction edges; entity edges, interaction nodes; entity and interaction edges, participant edges).
* Use node and properties to hold the fundamental type data.
