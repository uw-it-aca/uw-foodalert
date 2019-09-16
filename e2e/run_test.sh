#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker-compose -f $DIR/docker-compose.yml run taster
docker-compose -f $DIR/docker-compose.yml down

sudo chown -R $USER $DIR
sudo chgrp -R $(id -g) $DIR