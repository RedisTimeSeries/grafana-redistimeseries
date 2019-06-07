# RedisTimeSeries + Grafana + Grafana Redis source

## Run the stack

```bash
docker-compose up -d
```

## Setup Grafana

open the browser to url:

[http://localhost:3000](http://localhost:3000)

Default username and passwords are:
 - username: `admin`
 - password: `admin`

## Setup the data source in Grafana

- On dashboard, click `Add Data Source`

- Select `SimpleJson` datasource

- Name the source a recognizable name, like `RedisTimeSeries`

- In URL: enter `http://grafana_redis_source:8080` (the internal name for the service, exposed at port 8080)

- Click `Test and Save`

- It should show a green notification stating the connection worked.

## Create a Dashboard

- Go to Dashboards -> Home

- Click `New Dashboard`

- Click `Add Query`

- In Query Select the `RedisTimeSeries` data source you created earlier

- In the Query `timeserie` dropdown enter `temperature` which is the name of the key produced by the producer example.

- You should now see some data in the chart.

- Save the Dashboard with the top right Save icon (note this is saved in the container so config will be lost if you delete the container)
In order to save config, modify the `docker-compose.yml` file to mount a storage volume.

