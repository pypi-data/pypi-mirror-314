#!/bin/bash
set -euo pipefail

# The absolute path to this script.
SELF=$(readlink -f "${BASH_SOURCE[0]}")

# The project directory.
PROJECT_DIR=${SELF%/*/*}

# Source env.sh to configure the script's environment.
source "$PROJECT_DIR/env.sh"

# Run the passed command in the configured environment.
"$@"
