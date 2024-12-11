#!/bin/bash
set -euo pipefail

# The absolute path to this script.
SELF=$(readlink -f "${BASH_SOURCE[0]}")

# The project directory.
PROJECT_DIR=${SELF%/*/*}

# Source env.sh to configure the script's environment.
source "$PROJECT_DIR/env.sh"

# Install pylint in the virtual environment.
pip install pylint

# Run pylint on the source directory.
pylint "$PROJECT_DIR/src"
