#!/usr/bin/env bash
set -euo pipefail

# Set the working directory to this script's parent directory.
SELF=$(readlink -f "${BASH_SOURCE[0]}")
cd -- "${SELF%/*}"

# Run metabograph with this configuration file.
metabograph ./config.yaml tmp/graph.gml
