FROM node:12-buster-slim

USER node
WORKDIR /home/node

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

USER root
RUN apt-get update
RUN apt-get install -y wait-for-it /home/node/google-chrome-stable_current_amd64.deb

ARG curr_uid
RUN usermod -u ${curr_uid} node
RUN groupmod -g ${curr_uid} node
RUN usermod -d /home/node -m node

USER node
WORKDIR /home/node
RUN npm init --force
RUN npm install nightwatch chromedriver nightwatch-vrt

ADD --chown=node:node nightwatch.conf.js .
ADD --chown=node:node nightwatch.json .
ADD tests tests
ADD --chown=node:node vrt vrt
