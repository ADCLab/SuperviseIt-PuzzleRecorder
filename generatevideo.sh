#!/bin/bash

id_pattern="[0-9a-z]{10}"

for folder in $(ls | egrep -x "${id_pattern}"); do

	participantId=$folder
	bagfile="${folder}/${participantId}.bag"
	video="${folder}/${participantId}.mp4"
    
    # Convert if no cooresponding mp4
    if [[ ! -f $video ]]; then

        echo "Converting ${bagfile}"

        TMPDIR=$(mktemp -d)

        rs-convert -c -i "$bagfile" -p $TMPDIR/
        ffmpeg -loglevel quiet -r 30 -pattern_type glob -i "${TMPDIR}/*.png" "${folder}/${participantId}.mp4"

        rm -rf $TMPDIR
      	# rm $bagfile
    fi

done

