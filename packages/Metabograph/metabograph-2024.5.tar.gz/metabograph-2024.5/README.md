# Synopsis

Metabograph is a Python library for generating metabolic networks from [BioPAX](http://www.biopax.org/) data. The generated [NetworkX](https://networkx.org/) graphs can be used in various application such as training [graph neural networks (GNNs)](https://en.wikipedia.org/wiki/Graph_neural_network) or saved to files for use with viewers such as [Gephi](https://gephi.org/).


## Links

[insert: links]: #

## GitLab

* [Homepage](https://gitlab.inria.fr/jrye/metabograph)
* [Source](https://gitlab.inria.fr/jrye/metabograph.git)
* [Documentation](https://jrye.gitlabpages.inria.fr/metabograph)
* [Issues](https://gitlab.inria.fr/jrye/metabograph/-/issues)
* [GitLab package registry](https://gitlab.inria.fr/jrye/metabograph/-/packages)

## Other Repositories

* [Python Package Index](https://pypi.org/project/Metabograph/)

[/insert: links]: #



# Usage

## Configuration File

Metabograph uses a YAML configuration file to set the target species, configure eventual BioPAX SPARQL endpoints and filter graphs by cellular pathways and locations. A default configuration file with comments can be generated with the command `metabograph --create-config config.yaml`:

[insert: command_output:yaml metabograph --create-config -]: #

~~~yaml
# ConfigData

# BioPAX configuration.
biopax:
  # A list of paths to custom OWL files in the BioPAX level-3 format to use, either with or without the default files
  # depending on the value of include_default_owl_files.
  # Type: list[Path] [OPTIONAL]
  custom_owl_files: []

  # An optional URL to a SPARQL endpoint through which to query BioPAX data, such as a local Fuseki server.
  # Type: str [OPTIONAL]
  endpoint: null

  # If True, include complexes and their components.
  # Type: bool [OPTIONAL]
  include_complexes: true

  # If True, include the default BioPAX files for the configured species. These files will be downloaded if necessary.
  # Type: bool [OPTIONAL]
  include_default_owl_files: true

  # If True, include member entities (as defined by BioPAX).
  # Type: bool [OPTIONAL]
  include_member_entities: false

  # If True, items for which a pathway or location is unknown will be kept when filtering by pathway and/or location.
  # Type: bool [OPTIONAL]
  keep_unknown: false

  # Either a list of BioPax entity locations, or a path to a plaintext file with one location per line. See `metabograph
  # --list-locations` for the complete list.
  # Type: Union[list[str], str] [OPTIONAL]
  locations: null

  # Either a list of BioPAX pathways, or a path to a plaintext file with one pathways per line. See `metabograph --list-
  # pathways` for the complete list.
  # Type: Union[list[str], str] [OPTIONAL]
  pathways: null

  # The target species. It must be one supported by BioPAX. See `metabograph --list-species` for the complete list.
  # Type: str [OPTIONAL]
  species: homo sapiens

# Cache configuration.
cache:
  # The path to a cache directory. If unset, the standard XDG user cache directory will be used.
  # Type: Path [OPTIONAL]
  path: null

  # The timeout for the cached data. Data will be cleared from the cache after this timeout. If unset, cached data will
  # not automatically time out.
  # Type: int [OPTIONAL]
  timeout: null


~~~

[/insert: command_output:yaml metabograph --create-config -]: #

## Metabograph Command-Line Tool

The `metabograph` command-line tool can be used to query the available species, pathways and cellular localizations and generate graph files in [GML format](https://networkx.org/documentation/stable/reference/readwrite/gml.html).

[insert: command_output metabograph --help -]: #

~~~
usage: metabograph [-h] [--clear-cache] [--create-config PATH]
                   [--list-species] [--list-locations] [--list-pathways] [-v]
                   [config] [graph]

Generate graphs from Reactome BioPAX data.

positional arguments:
  config                Path to the YAML configuration file.
  graph                 Output path for the generated graph in GML format.

options:
  -h, --help            show this help message and exit
  --clear-cache         Clear the cache to force a refresh of query data.
  --create-config PATH  Create a YAML configuration file at the given path. If
                        the path is "-", the generated YAML will be printed to
                        STDOUT.
  --list-species        List available species.
  --list-locations      List recognized cellular locations.
  --list-pathways       List recognized pathways.
  -v, --verbose         Increasing logging level to DEBUG. Pass twice to also
                        show SPARQL queries.

~~~

[/insert: command_output metabograph --help -]: #

## Python API

For the full API, see the API documentation linked above. The following is an example of common basic usage.

~~~python
# Import the required modules.
from metabograph.config import Config
from metabograph.biopax.query_manager import BiopaxQueryManager
from metabograph.biopax.graph_generator import BiopaxGraphGenerator

# Instantiate a configuration file from a file (or manually).
config = Config(path="config.yaml")

# Instantiate a query manager.
bqm = BiopaxQueryManager(config)

# Get the lists of species, pathways and cellular locations.
species = bqm.list_species()
pathways = bqm.list_pathways()
locations = bqm.list_locations()

# Instantiate a graph generator and get the networkx graph object for the
# current configuration.
bgg = BiopaxGraphGenerator(bqm=bqm)
graph = bgg.get_graph()

# Do stuff with the graph...
print(graph)
# ...
~~~


## Fuseki Server

[Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) is a third-party server that provides faster parsing of OWL files than the Python packages `owlready2` and `rdflib`. The script [download_fuseki.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/scripts/download_fuseki.sh) is provided to quickly download the source code and create a configuration file for running the server locally.

By default, the script will download files to the directory `tmp/fuseki` and write required environment variables to `tmp/fuseki/env.sh`. These environment variables can be can be loaded manually in a Bash shell via the command `source tmp/fuseki/env.sh`. 

The [env.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/env.sh) file mentioned above will run `download_fuseki.sh` if necessary and set the Fuseki environment variables.

Once the environment variables have been set, the Fuseki server can be run in a terminal via the command `metabograph-fuseki`.

The easiest way to run the local Fuseki server regardless of the user's current shell is to run the following command:

~~~sh
./scripts/run_in_venv.sh metabograph-fuseki <path_to_config>
~~~

Replace `<path_to_config>` with the path to the Metabograph configuration file that will be used with Metabograph. See the `metabograph-fuseki` help message for further options:

[insert: command_output metabograph-fuseki --help -]: #

~~~
usage: metabograph-fuseki [-h] [-v] config

Run the Fuseki server.

positional arguments:
  config         The Metabograph configuration file.

options:
  -h, --help     show this help message and exit
  -v, --verbose  Show debug messages.

~~~

[/insert: command_output metabograph-fuseki --help -]: #


## Examples

Examples can be found in the [examples directory](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/examples).


## NVIDIA cuGraph

[NVIDIA cuGraph](https://developer.nvidia.com/blog/networkx-introduces-zero-code-change-acceleration-using-nvidia-cugraph/) is a drop-in alternative backend for [NetworkX](https://networkx.org/) that claims significant speedups without any code changes. To use it, install the appropriate [nx-cugraph package](https://pypi.org/search/?q=nx-cugraph) in the same environment as Metabograph (e.g. via `pip`) and then export the environment variable`NX_CUGRAPH_AUTOCONFIG=True`before running your code:

~~~sh
export NX_CUGRAPH_AUTOCONFIG=True
./your_code.py

# OR
NX_CUGRAPH_AUTOCONFIG=True ./your_code.py
~~~


## Utilities

The project provides the following files and scripts for convenience. See the dependencies below.

* [env.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/env.sh) - A Bash file that can be sourced to do the following:

    - Create and configure a Python virtual environment.
    - Download and unpack the Fuseki server.
    * Activate the Python virtual environment and configure the Fuseki environment variables.

* [build_doc.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/scripts/build_doc.sh) - Build the Python documentation with Sphinx.
* [create_venv.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/scripts/create_venv.sh) - Create a Python virtual environment with Metabograph installed in editable mode.
* [download_fuseki.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/scripts/download_fuseki.sh) - Download the Fuseki server and unpack it to a temporary directory. This will also generate a file with the required environment variables for using the server.
* [pylint.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/scripts/pylint.sh) - Run Pylint on the Metabograph source code.
* [run_in_venv.sh](https://gitlab.inria.fr/jrye/metabograph/-/tree/main/scripts/run_in_venv.sh) - Run a command in the fully configured virtual environment. This should by used by users of non-Bash shells who do not wish to manually configure their own environments. The script will run any command passed to it: `run_in_venv.sh command arg1 arg2 ...`.

### Dependencies

* [Bash](https://www.gnu.org/software/bash/bash.html) version 5.0 or newer.
* bsdtar from [libarchive](https://libarchive.org/) (available in the `libarchive-tools` package on Ubuntu).


# References

* [BioPAX](https://www.biopax.org/owldoc/Level3/)
