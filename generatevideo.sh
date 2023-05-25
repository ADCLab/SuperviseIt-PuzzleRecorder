#!/bin/bash

for file in $(ls *.bag); do

    # Get id
    participantId="$(basename -s .bag $file)"
    
    # Convert if no cooresponding mp4
    if [[ ! -f "${participantId}.mp4" ]]; then
        echo "Converting ${file}"

        TMPDIR=$(mktemp -d)

        rs-convert -c -i "$file" -p $TMPDIR/
        ffmpeg -loglevel quiet -r 30 -pattern_type glob -i "${TMPDIR}/*.png" "${participantId}.mp4"

        rm -rf $TMPDIR
    fi
done

