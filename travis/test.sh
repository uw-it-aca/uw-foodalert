#!/bin/sh
set -e
trap 'exit 1' ERR

# travis test script for django app
#
# PRECONDITION: inherited env vars from application's .travis.yml MUST include:
#      DJANGO_APP: django application directory name

# start virtualenv
source bin/activate

# install test tooling
pip install pycodestyle coverage
apt-get install -y nodejs npm gcc-4.8 unixodbc-dev
npm install .
npm install eslint eslint-config-google eslint-plugin-vue eslint-plugin-vue-a11y eslint-config-stylelint

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

run_test "pycodestyle ${DJANGO_APP}/ --exclude=migrations,static"
run_test "./node_modules/.bin/eslint --ext .js,.vue ${DJANGO_APP}/static/${DJANGO_APP}/js/"
run_test "coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

# put generaged coverage result where it will get processed
cp .coverage.* /coverage

exit 0