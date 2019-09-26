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

COPY --chown=node:node package.json package.json
COPY --chown=node:node package-lock.json package-lock.json
COPY --chown=node:node docker-compose.yml docker-compose.yml
COPY --chown=node:node cypress.json cypress.json
COPY --chown=node:node cypress cypress

RUN npm install .