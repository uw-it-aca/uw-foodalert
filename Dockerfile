FROM acait/django-container:feature-refactor as django

USER root
RUN apt-get install -y libpq-dev
USER acait

ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
ADD --chown=acait:acait README.md /app/

ADD --chown=acait:acait docker /app/project/
ENV DB postgres

RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/

RUN rm -rf /app/foodalert/static/foodalert/bundles && mkdir /app/foodalert/static/foodalert/bundles

FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack
ENV AUTH SAML_MOCK

FROM django 

COPY --chown=acait:acait --from=wpack /app/foodalert/static/foodalert/bundles/* /app/foodalert/static/foodalert/bundles/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/ /static/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/webpack-stats.json /app/foodalert/static/webpack-stats.json
