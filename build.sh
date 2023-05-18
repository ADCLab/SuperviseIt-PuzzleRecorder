#!/bin/bash

# Check for the google sheets credentials json file
if [[ ! -f sheetsCredentials.json ]]; then
    echo sheetsCredentials.json not found.
    exit 1
fi

# Generate executable
pyinstaller -F -w --clean -n "Cluster Tracking" -i "TheTab_KGrgb_72ppi.ico" --add-data "TheTab_KGrgb_72ppi.png:." src/main.py