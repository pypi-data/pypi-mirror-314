#!/usr/bin/env bash

# The absolute path to this file.
METABOGRAPH_ENV_SH=$(readlink -f "${BASH_SOURCE[0]}")

# The project directory.
METABOGRAPH_PROJ_DIR=${METABOGRAPH_ENV_SH%/*}

# The scripts directory.
METABOGRAPH_SCRIPTS_DIR=$METABOGRAPH_PROJ_DIR/scripts



# The default virtual environment directory.
METABOGRAPH_VENV_DIR=$METABOGRAPH_PROJ_DIR/venv

# Create the virtual environment if necessary.
if [[ ! -e $METABOGRAPH_VENV_DIR ]]
then
  "$METABOGRAPH_SCRIPTS_DIR/create_venv.sh"
fi

# Activate the virtual environment.
source "$METABOGRAPH_VENV_DIR/bin/activate"



# The Fuseki directory.
METABOGRAPH_FUSEKI_DIR=$METABOGRAPH_PROJ_DIR/tmp/fuseki

# The Fuseki environment variable file. 
METABOGRAPH_FUSEKI_ENV_SH=$METABOGRAPH_FUSEKI_DIR/env.sh

# Download Fuseki if necessary.
if [[ ! -e $METABOGRAPH_FUSEKI_ENV_SH ]]
then
  "$METABOGRAPH_SCRIPTS_DIR/download_fuseki.sh" -d "$METABOGRAPH_FUSEKI_DIR"
fi

# Source the Fuseki environment file.
source "$METABOGRAPH_FUSEKI_ENV_SH"


# Print information about current configuration.
cat << INFO
Successfully sourced environment file.

  Python virtual environment: $VIRTUAL_ENV
  Fuseki directory: $FUSEKI_HOME
  JVM_ARGS: ${JVM_ARGS:-}

Run "deactivate" to deactivate the Python virtual environment.

INFO
