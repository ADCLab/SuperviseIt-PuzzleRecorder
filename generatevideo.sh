#!/bin/bash

TMPDIR=$(mktemp -d)

rs-convert -i test.bag -p $TMPDIR/ -c
ffmpeg -r 30 -pattern_type glob -i "${TMPDIR}/*.png" video.mp4

rm -rf $TMPDIR
