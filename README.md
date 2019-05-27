# RedisTimeSeries-Datasource
Grafana Datasource for RedisTimeSeries


## Grafana Datastore API Server
### Overview
A HTTP Server to serve metrics to Grafana via the simple-json-datasource

### Grafana configuration

1. install SimpleJson data source: https://grafana.net/plugins/grafana-simple-json-datasource/installation
2. in Grafana UI, go to Data Sources
3. Click `Add data source`
    3.1 choose Name
    3.2 Type: `SimpleJson`
    3.3 URL: point to the URL for your GrafanaDatastoreServer.py
    3.4 Access: direct (unless you are using a proxy)

4. Query the datasource by a specific key, or * for a wildcard, for example: `stats_counts.http.*`

### GrafanaDatastoreServer.py Usage
```
usage: GrafanaDatastoreServer.py [-h] [--host HOST] [--port PORT]
                                 [--redis-server REDIS_SERVER]
                                 [--redis-port REDIS_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           server address to listen to
  --port PORT           port number to listen to
  --redis-server REDIS_SERVER
                        redis server address
  --redis-port REDIS_PORT
                        redis server port
```
