# Synopsis

This example generates a graph from [Sertbaş2014 - Brain specific metabolic network (iMS570)](https://www.ebi.ac.uk/biomodels/MODEL1401240000#Files). It uses a custom subclass of BiopaxGraphGenerator to ensures that reaction pathways are connected via entities and to add custom node attributes such as the cell type.

# Usage

Run the [sertbas2014.py](sertbas2014.py) script to download the required data and generate the graph GML file, which can be viewed with a viewer such as [Gephi](https://gephi.org/).

![Gephi example](img/sertbas2014-gephi.png)

Examine the script for details of how to customize node attributes.

