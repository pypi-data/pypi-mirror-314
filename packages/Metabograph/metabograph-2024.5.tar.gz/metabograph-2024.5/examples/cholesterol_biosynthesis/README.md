# Synopsis

Generate a graph of the cholesterol biosynthesis pathway using standard BioPAX data from [Reactome](https://reactome.org/). The generated graph can be compared to [the corresponding graph on Reactome](https://reactome.org/PathwayBrowser/#/R-HSA-191273).

# Usage

The provided [cholesterol_biosynthesis.sh](cholesterol_biosynthesis.sh) script simply runs the command `metabograph config.yaml tmp/graph.gml` in the same directory as the configuration file. The resulting graph can be viewed with a viewer such as [Gephi](https://gephi.org/):

![Gephi example](img/cholesterol_biosynthesis.png)


The example is a bit slow due to direct loading of the BioPAX OWL files via Python libraries. To increase the speed, set the BioPAX endpoint in the configuration file to e.g. `http://localhost:3030` and then in a separate terminal run the local Fuseki server with `metabograph-fuseki config.yaml`. This should significantly speed up the graph generation.
