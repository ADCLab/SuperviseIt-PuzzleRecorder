#!/bin/bash

# Removes all .log files, .bag files, .csv files, and snapshots,
for file in $(ls | egrep "*.(log|bag|csv)|Snapshot[0-5].png"); do
    rm $file
done
