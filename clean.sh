#!/bin/bash

REMOVE_BAG=false
REMOVE_CSV=false
REMOVE_LOG=false
REMOVE_MP4=false
REMOVE_PNG=false

while [[ $1 != "" ]]; do

    case $1 in
        -a | --all)
            REMOVE_BAG=true
            REMOVE_CSV=true
            REMOVE_LOG=true
            REMOVE_MP4=true
            REMOVE_PNG=true
            break 2
            ;;

        --all-except)

            REMOVE_BAG=true
            REMOVE_CSV=true
            REMOVE_LOG=true
            REMOVE_MP4=true
            REMOVE_PNG=true

            shift
            while [[ $1 != "" ]]; do
                case $1 in
                    bag) 
                        REMOVE_BAG=false
                        ;;
                    csv)
                        REMOVE_CSV=false
                        ;;
                    log)
                        REMOVE_LOG=false
                        ;;
                    mp4)
                        REMOVE_MP4=false
                        ;;
                    png)
                        REMOVE_PNG=false
                        ;;
                esac
                shift
            done    
            
            break 2
            ;;

        -b | --bag)
            REMOVE_BAG=true
            ;;
        -c | --csv)
            REMOVE_CSV=true
            ;;
        -l | --log)
            REMOVE_LOG=true
            ;;
        -m | --mp4)
            REMOVE_MP4=true
            ;;
        -p | --png)
            REMOVE_PNG=true
            ;;
    esac
    shift
done

id_pattern="[0-9a-z]{10}"
for file in *; do

    if [[ $REMOVE_BAG == true && $(echo "$file" | egrep -x "${id_pattern}\.bag") ]]; then
        rm "$file"
    fi
    if [[ $REMOVE_CSV == true && $(echo "$file"| egrep -x "${id_pattern}\.csv") ]]; then
        rm "$file"
    fi
    if [[ $REMOVE_LOG == true && $(echo "$file" | egrep -x "20[0-9]{2}-(0[1-9]|1[0-2])-((0|1|2)[0-9]|3[0-1])-((0|1)[0-9]|2[0-3])_[0-5][0-9]_[0-5][0-9]\.log") ]]; then
        rm "$file"
    fi
    if [[ $REMOVE_MP4 == true && $(echo "$file" | egrep -x "${id_pattern}\.mp4") ]]; then
        rm "$file"
    fi
    if [[ $REMOVE_PNG == true && $(echo "$file" | egrep -x "${id_pattern}_(0|[A-E])\.png") ]]; then
        rm "$file"
    fi

done