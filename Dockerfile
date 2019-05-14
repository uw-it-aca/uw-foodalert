# Arg for settings which container is final
ARG BUILD_STAGE=deploy


#### INSTALLATION CONTAINERS

## Django container with app installed
FROM acait/django-container:feature-refactor as django
ENV AUTH SAML_MOCK
# Install deps as root
USER root
RUN apt-get install -y libpq-dev
# Switch to acait and chown setup files
USER acait
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
ADD --chown=acait:acait README.md /app/
ADD --chown=acait:acait docker /app/project/
# Install
RUN . /app/bin/activate && pip install -r requirements.txt
# Add and chown app files
ADD --chown=acait:acait . /app/
# Clear out space for statics
RUN rm -rf /app/foodalert/static/foodalert/bundles && mkdir /app/foodalert/static/foodalert/bundles

## Container with compiled statics
FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack


#### TEST CONTAINERS

## Container that runs python tests and outputs coverage
FROM django AS testpy
RUN chmod +x bin/activate
RUN bin/pip install python-coveralls
RUN bin/pip install coverage==4.5.3
RUN bin/pip install pycodestyle
RUN bin/pycodestyle foodalert/ --exclude=migrations
RUN bin/activate && bin/coverage run --rcfile=$(pwd)/.coveragerc --omit=foodalert/migrations/* manage.py test foodalert

## Container that runs js tests and outputs coverage
FROM wpack AS testjs
RUN apt-get update
RUN apt-get install ruby-full -y
RUN gem install coveralls-lcov
RUN npx jest --coverage && coveralls-lcov -v -n ./coverage/lcov.info > js-coverage.json


#### FILE COLLATION CONTAINERS

## The final container with the app installed and compiled static files
FROM django AS deploy
COPY --chown=acait:acait --from=wpack /app/foodalert/static/foodalert/bundles/* /app/foodalert/static/foodalert/bundles/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/ /static/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/webpack-stats.json /app/foodalert/static/webpack-stats.json

## The final test container with both coverage files
FROM testpy AS test
RUN bin/pip install coveralls
COPY --from=testjs /app/js-coverage.json .


#### CONTAINER SELECTION

## Selector between different final containers
FROM ${BUILD_STAGE}
