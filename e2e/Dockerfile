FROM cypress/browsers:node12.6.0-chrome75

USER root

ARG curr_uid
ARG curr_gid
RUN usermod -u ${curr_uid} node
RUN groupmod -g ${curr_gid} node
RUN usermod -d /home/node -m node

USER node
WORKDIR /home/node
RUN mkdir e2e
WORKDIR /home/node/e2e

ADD package.json package.json

RUN npm install .