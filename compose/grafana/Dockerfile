FROM grafana/grafana

RUN grafana-cli plugins install grafana-simple-json-datasource

ADD ./config.ini /etc/grafana/config.ini
ADD ./provisioning/datasources/redistimeseries.yaml /etc/grafana/provisioning/datasources/redistimeseries.yaml
