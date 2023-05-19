#!/bin/bash

PROGRAM_NAME="Cluster_Tracking"

# Check for the google sheets credentials json file
if [[ ! -f sheetsCredentials.json ]]; then
    echo sheetsCredentials.json not found.
    exit 1
fi

# Set up the virtual environment
if [[ ! -d ./.venv/ ]]; then
    python -m venv .venv
fi

source ./.venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# Generate the executable
TMPDIR_DIST=$(mktemp -d)
TMPDIR_BUILD=$(mktemp -d)

pyinstaller -F -w --clean --name "${PROGRAM_NAME}" --add-data "src/TheTab_KGrgb_72ppi.png:./src" src/main.py --distpath "${TMPDIR_DIST}" --workpath "${TMPDIR_BUILD}"
mv "${TMPDIR_DIST}/${PROGRAM_NAME}" "."

rm -rf $TMPDIR_DIST $TMPDIR_BUILD
