#!/bin/bash

mkdir frames
rs-convert -i test.bag -p frames/

ffmpeg -r 30 -pattern_type glob -i 'frames/*.png' video.mp4

rm -rf frames
