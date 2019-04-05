FROM node:8.15.1-jessie AS wpack
ADD . /app/
WORKDIR /app/
RUN npm install .
RUN npx webpack

FROM acait/django-container:python3
RUN mkdir /app/logs
ADD setup.py /app/
ADD requirements.txt /app/
ADD README.md /app/
RUN apt-get install -y libpq-dev
RUN . /app/bin/activate && pip install -r requirements.txt
ADD /docker/web/apache2.conf /tmp/apache2.conf
RUN rm -rf /etc/apache2/sites-available/ && mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf &&\
    mkdir /etc/apache2/logs
ADD . /app/
RUN rm -rf /app/foodalert/static/foodalert/bundles && mkdir /app/foodalert/static/foodalert/bundles
COPY --from=wpack /app/foodalert/static/foodalert/bundles/* /app/foodalert/static/foodalert/bundles/
COPY --from=wpack /app/foodalert/static/ /static/
COPY --from=wpack /app/project/webpack-stats.json /app/project/webpack-stats.json
ENV DB postgres
ADD docker /app/project/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh" ]
