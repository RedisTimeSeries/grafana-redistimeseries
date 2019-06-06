#!/usr/bin/env python

import argparse
import math
import random
from time import sleep
from redistimeseries.client import Client as RedisTimeSeries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--redis-server", help="redis server address", default="localhost")
    parser.add_argument("--redis-port", help="redis server port", default=6379, type=int)
    args = parser.parse_args()
    print("""
    Starting with:
    redis server: {}
    redis port: {}
    """.format(args.redis_server, args.redis_port))

    rts = RedisTimeSeries(port=args.redis_port, host=args.redis_server)

    try:
        rts.create('temperature', retentionSecs=60*24, labels={'sensorId': '2'})
    except Exception as e:
        # will except if key already exists (i.e. on restart)
        print(str(e))

    variance = 0
    t = 0
    while True:
        # add with current timestamp
        print(".", end="")
        variance += (random.random() - 0.5) / 10.0
        t += 1
        value = math.cos(t / 100) + variance
        rts.add('temperature', '*', value)
        sleep(0.1)


if __name__ == '__main__':
    main()
