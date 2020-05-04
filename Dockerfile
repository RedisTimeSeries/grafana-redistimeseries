FROM python:3-alpine


WORKDIR /app/

COPY requirements.txt /app/

RUN apk update && apk add --no-cache --virtual build-deps build-base gcc musl-dev libffi-dev libev-dev
RUN pip install -r requirements.txt
RUN apk del build-deps

COPY GrafanaDatastoreServer.py /app/

EXPOSE 8080
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

CMD /app/GrafanaDatastoreServer.py --redis-server $REDIS_HOST --redis-port $REDIS_PORT
