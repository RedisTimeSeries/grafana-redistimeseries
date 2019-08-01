#!/usr/bin/env python

import argparse
import redis
import flask
from datetime import timedelta, datetime
import dateutil.parser
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

EPOCH = datetime(1970, 1, 1, 0, 0, 0)

REDIS_POOL = None
SCAN_TYPE_SCRIPT = """local cursor, pat, typ, cnt = ARGV[1], ARGV[2], ARGV[3], ARGV[4] or 100
local rep = {}

local res = redis.call('SCAN', cursor, 'MATCH', pat, 'COUNT', cnt)
while #res[2] > 0 do
  local k = table.remove(res[2])
  local t = redis.call('TYPE', k)
  if t['ok'] == typ then
    table.insert(rep, k)
  end
end

rep = {tonumber(res[1]), rep}
return rep"""

@app.route('/')
@cross_origin()
def hello_world():
    return 'OK'

@app.route('/search', methods=["POST", 'GET'])
@cross_origin()
def search():
    redis_client = redis.Redis(connection_pool=REDIS_POOL)
    result = []
    cursor = 0
    while True:
        cursor, keys = redis_client.eval(SCAN_TYPE_SCRIPT, 0, cursor, "*", "TSDB-TYPE", 100)
        result.extend(keys)
        if cursor == 0:
            break

    return jsonify(result)

def process_targets(targets, redis_client):
    result = []
    for target in targets:
        if '*' in target:
            result.extend(redis_client.keys(target))
        else:
            result.append(target)
    return result

@app.route('/query', methods=["POST", 'GET'])
def query():
    request = flask.request.get_json()
    response = []

    # !!! dates 'from' and 'to' are expected to be in UTC, which is what Grafana provides here.
    # If not in UTC, use pytz to set to UTC timezone and subtract the utcoffset().
    # Time delta calculations should always be done in UTC to avoid pitfalls of daylight offset changes.
    stime = (dateutil.parser.parse(request['range']['from']) - EPOCH) / timedelta(milliseconds=1)
    etime = (dateutil.parser.parse(request['range']['to']) - EPOCH) / timedelta(milliseconds=1)

    redis_client = redis.Redis(connection_pool=REDIS_POOL)
    targets = process_targets([t['target'] for t in request['targets']], redis_client)

    for target in targets:
        args = ['ts.range', target, int(stime), int(etime)]
        if 'intervalMs' in request and request['intervalMs'] > 0:
            args += ['avg', int(request['intervalMs'])]
        print(args)
        redis_resp = redis_client.execute_command(*args)
        datapoints = [(float(x2.decode("ascii")), x1) for x1, x2 in redis_resp]
        response.append(dict(target=target, datapoints=datapoints))
    return jsonify(response)


@app.route('/annotations')
def annotations():
    return jsonify([])

def main():
    global REDIS_POOL
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="server address to listen to", default="0.0.0.0")
    parser.add_argument("--port", help="port number to listen to", default=8080, type=int)
    parser.add_argument("--redis-server", help="redis server address", default="localhost")
    parser.add_argument("--redis-port", help="redis server port", default=6379, type=int)
    args = parser.parse_args()

    REDIS_POOL = redis.ConnectionPool(host=args.redis_server, port=args.redis_port)

    http_server = WSGIServer(('', args.port), app)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
