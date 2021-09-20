FROM gcr.io/uwit-mci-axdd/django-container:1.3.3 as app-container

USER root
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN apt-get install -y postgresql-client-10
USER acait

ADD --chown=acait:acait foodalert/VERSION /app/foodalert/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
ADD --chown=acait:acait README.md /app/

ADD --chown=acait:acait docker/scripts /scripts/
ADD --chown=acait:acait docker /app/project/

RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

RUN rm -rf /app/foodalert/static/foodalert/bundles && mkdir /app/foodalert/static/foodalert/bundles

FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.3 as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/

FROM app-container

COPY --chown=acait:acait --from=wpack /app/foodalert/static/foodalert/bundles/* /app/foodalert/static/foodalert/bundles/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/ /static/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/webpack-stats.json /app/foodalert/static/webpack-stats.json