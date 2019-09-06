FROM node:12-buster

USER node
WORKDIR /home/node

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

USER root
RUN apt-get update
RUN apt-get install -y /home/node/google-chrome-stable_current_amd64.deb

USER node
WORKDIR /home/node
RUN npm init --force
RUN npm install nightwatch chromedriver nightwatch-vrt

ADD --chown=node:node nightwatch.conf.js .
ADD --chown=node:node nightwatch.json .
ADD --chown=node:node wait-for-it.sh .
ADD tests tests
ADD --chown=node:node vrt vrt
