FROM python:alpine3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY producer.py /app/

ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

CMD /app/producer.py --redis-server $REDIS_HOST --redis-port $REDIS_PORT
