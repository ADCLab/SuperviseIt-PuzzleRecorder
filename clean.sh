#!/bin/bash

# Removes all .log files, .bag files, .csv files, snapshots, and mp4 files
for file in $(ls | egrep "*.(log|bag|csv|mp4)|Snapshot[0-5].png"); do
    rm $file
done
