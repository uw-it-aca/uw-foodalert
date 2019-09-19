#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -n "$1" ]; then
    case "$1" in
 
    -b) USERID=$(id -u) GROUPID=$(id -g) docker-compose -f $DIR/docker-compose.yml build $2 ;;

    *) echo "Option $1 not recognized" ;;

    esac
 
    shift
fi

USERID=$(id -u) GROUPID=$(id -g) docker-compose -f $DIR/docker-compose.yml run taster
USERID=$(id -u) GROUPID=$(id -g) docker-compose -f $DIR/docker-compose.yml down