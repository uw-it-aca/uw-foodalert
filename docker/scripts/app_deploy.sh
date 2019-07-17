#!bin/bash

ls /app/foodalert/fixtures | while read fixture
do
    echo "Loading fixture $fixture..."
    /app/bin/python /app/manage.py loaddata $fixture
done
