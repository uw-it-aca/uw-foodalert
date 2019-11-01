FROM acait/django-container:1.0.10 as django

USER root
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN apt-get install -y postgresql-client-10
ADD docker/info.conf /tmp/info.conf
RUN cp /tmp/info.conf /etc/apache2/conf-enabled/
ADD docker/remoteip.conf /tmp/remoteip.conf
RUN cp /tmp/remoteip.conf /etc/apache2/conf-enabled/
ADD docker/log_forensic.conf /tmp/log_forensic.conf
RUN cp /tmp/log_forensic.conf /etc/apache2/conf-enabled/
USER acait

ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
ADD --chown=acait:acait README.md /app/

ADD --chown=acait:acait docker/scripts /scripts/
ADD --chown=acait:acait docker /app/project/

RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/

RUN rm -rf /app/foodalert/static/foodalert/bundles && mkdir /app/foodalert/static/foodalert/bundles

FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack


FROM django

COPY --chown=acait:acait --from=wpack /app/foodalert/static/foodalert/bundles/* /app/foodalert/static/foodalert/bundles/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/ /static/
COPY --chown=acait:acait --from=wpack /app/foodalert/static/webpack-stats.json /app/foodalert/static/webpack-stats.json
