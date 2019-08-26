#!bin/bash

/app/bin/python /app/manage.py migrate

if [ "$ENV" == "localdev" ]; then
    chmod +x docker/scripts/app_deploy.sh
    . docker/scripts/app_deploy.sh
fi