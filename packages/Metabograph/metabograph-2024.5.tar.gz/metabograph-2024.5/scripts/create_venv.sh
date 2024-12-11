#!/bin/bash
set -euo pipefail

# The absolute path to this script.
SELF=$(readlink -f "${BASH_SOURCE[0]}")

# The project directory.
PROJECT_DIR=${SELF%/*/*}

# The virtual environment directory.
VENV_DIR=$PROJECT_DIR/venv

# Create the virtual environment if it doesn't exist.
python3 -m venv "$VENV_DIR"

# Activate the virtual environment.
activate_cmd=(source "$VENV_DIR/bin/activate")
"${activate_cmd[@]}"

# Upgrade pip in the virtual environment.
pip install --upgrade pip

# Install Metabograph with all of its dependencies.
pip install -U -e "${PROJECT_DIR}[extra]"

# Print instructions to activate the virtual environment.
cat << INSTRUCTIONS
Run the following command to activate the virtual environment in your terminal.

  ${activate_cmd[*]@Q}

INSTRUCTIONS
