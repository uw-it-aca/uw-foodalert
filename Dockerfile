FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack

FROM uw-foodalert_app
COPY --from=wpack /app/foodalert/static/foodalert/bundles/* /app/foodalert/static/foodalert/bundles/
COPY --from=wpack /app/foodalert/static/ /static/
COPY --from=wpack /app/foodalert/static/webpack-stats.json /app/foodalert/static/webpack-stats.json
