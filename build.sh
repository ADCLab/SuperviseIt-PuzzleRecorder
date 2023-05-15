#!/bin/bash

pyinstaller -F -w --clean -n "Cluster Tracking" -i "TheTab_KGrgb_72ppi.ico" --add-data "TheTab_KGrgb_72ppi.png:." src/main.py