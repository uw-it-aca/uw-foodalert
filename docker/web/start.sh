#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*

source "/app/bin/activate"

python3 manage.py migrate

pip3 install -r requirements.txt

rm -rf /static/
python3 manage.py collectstatic --noinput

# Start Apache server in foreground
exec /usr/sbin/apachectl -DFOREGROUND
