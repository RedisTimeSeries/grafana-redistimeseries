FROM python:alpine3.9

WORKDIR /app/

COPY requirements.txt /app/
RUN apk add --no-cache --virtual build-deps gcc musl-dev libffi-dev \
    && pip install -r requirements.txt \
    && apk del build-deps

COPY GrafanaDatastoreServer.py /app/

EXPOSE 8080
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

CMD /app/GrafanaDatastoreServer.py --redis-server $REDIS_HOST --redis-port $REDIS_PORT