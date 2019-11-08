#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

updateSnapshots=false

while getopts "ub" opt; do
    case "$opt" in

    u) updateSnapshots=true ;;

    b) USERID=$(id -u) GROUPID=$(id -g) UPDATE_SNAPSHOTS=$updateSnapshots docker-compose -f $DIR/docker-compose.yml build $2 ;;
    
    esac
done

USERID=$(id -u) GROUPID=$(id -g) UPDATE_SNAPSHOTS=$updateSnapshots docker-compose -f $DIR/docker-compose.yml run cypress
USERID=$(id -u) GROUPID=$(id -g) UPDATE_SNAPSHOTS=$updateSnapshots docker-compose -f $DIR/docker-compose.yml down