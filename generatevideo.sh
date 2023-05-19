#!/bin/bash

if [[ $1 == "" ]]; then
    echo Please provide bag file
    exit 1
fi

TMPDIR=$(mktemp -d)

rs-convert -i $1 -p $TMPDIR/ -c
ffmpeg -r 30 -pattern_type glob -i "${TMPDIR}/*.png" $(basename -s .bag "$1").mp4

rm -rf $TMPDIR
