# Data Streaming with Apache Kafka

Here, we construct a streaming event pipeline around Apache Kafka and its ecosystem. 

Using public data from the [Chicago Transit Authority](https://www.transitchicago.com/data/) we construct an event pipeline around Kafka that allows us to simulate and display the status of train lines in real time.

A simple dashboard summarises the data collected and processed, showing trains move from station to station.

![Final User Interface](images/ui.gif)


## Prerequisites

The following are required to complete this project:

* Docker
* Python 3.7
* Access to a computer with a minimum of 16gb+ RAM and a 4-core CPU to execute the simulation

## Description


The architecture looks like so:

![Project Architecture](images/diagram.png)

### Kafka Producers

Configure the train stations to emit events. The CTA has placed a sensor on each side of every train station that can be programmed to take an action whenever a train arrives at the station.

#### Python Producers

Python clients are set up to send data to Kafka regarding train and passenger information.

* A topic is created for each station in Kafka to track the arrival events. The station emits an `arrival` event to Kafka whenever the `Station.run()` function is called.
* A topic is created for each turnstile for each station in Kafka to track the turnstile events. The station emits a `turnstile` event to Kafka whenever the `Turnstile.run()` function is called.

#### Kafka REST Proxy Producer

Weather readings are sent into Kafka from weather hardware. We use HTTP REST to send the data to Kafka from the hardware using Kafka's REST Proxy.

* A topic is created for weather events. The weather model emits `weather` event to Kafka REST Proxy whenever the `Weather.run()` function is called.

#### Kafka Connect

Finally, we extract station information from a PostgreSQL database into Kafka. We use the [Kafka JDBC Source Connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/index.html) to push changes from the database to Kafka.

To accomplish this, you must complete the following tasks:



### Stream Processing 

We transform and aggregate the raw data in a streaming fashion

#### Faust Stream Processor

We leverage Faust Stream Processing to transform the raw Stations table that we ingested from Kafka Connect. The raw format from the database has more data than we need, and the line color information is not conveniently configured. To remediate this, we're going to ingest data from the Kafka Connect topic, and transform the data.



`faust -A faust_stream worker -l info`

### Configure the KSQL Table

We use KSQL to aggregate turnstile data for each of the stations. The turnstile data consists of simply an emmited event, not a count. What would make this data more useful would be to summarize it by station so that downstream applications always have an up-to-date count




###  Kafka Consumers
With all of the data in Kafka, we consume the data in the web server that is going to serve the transit status dashboard. All consumers are python clients.



### Documentation

* [Confluent Python Client Documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/#)
* [Confluent Python Client Usage and Examples](https://github.com/confluentinc/confluent-kafka-python#usage)
* [REST Proxy API Reference](https://docs.confluent.io/current/kafka-rest/api.html#post--topics-(string-topic_name))
* [Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html)

## Directory Layout
The project consists of two main directories, `producers` and `consumers`.


```

├── consumers
│   ├── consumer.py 
│   ├── faust_stream.py 
│   ├── ksql.py 
│   ├── models
│   │   ├── lines.py
│   │   ├── line.py 
│   │   ├── station.py 
│   │   └── weather.py 
│   ├── requirements.txt
│   ├── server.py
│   ├── topic_check.py
│   └── templates
│       └── status.html
└── producers
    ├── connector.py 
    ├── models
    │   ├── line.py
    │   ├── producer.py 
    │   ├── schemas
    │   │   ├── arrival_key.json
    │   │   ├── arrival_value.json 
    │   │   ├── turnstile_key.json
    │   │   ├── turnstile_value.json 
    │   │   ├── weather_key.json
    │   │   └── weather_value.json 
    │   ├── station.py 
    │   ├── train.py
    │   ├── turnstile.py 
    │   ├── turnstile_hardware.py
    │   └── weather.py 
    ├── requirements.txt
    └── simulation.py
```

## Running and Testing

To run the simulation, you must first start up the Kafka ecosystem utilizing Docker Compose.

```%> docker-compose up```

Docker compose will take a 3-5 minutes to start, depending on your hardware. Please be patient and wait for the docker-compose logs to slow down or stop before beginning the simulation.

Once docker-compose is ready, the following services will be available:

| Service | Host URL | Docker URL | Username | Password |
| --- | --- | --- | --- | --- |
| Public Transit Status | [http://localhost:8888](http://localhost:8888) | n/a | ||
| Landoop Kafka Connect UI | [http://localhost:8084](http://localhost:8084) | http://connect-ui:8084 |
| Landoop Kafka Topics UI | [http://localhost:8085](http://localhost:8085) | http://topics-ui:8085 |
| Landoop Schema Registry UI | [http://localhost:8086](http://localhost:8086) | http://schema-registry-ui:8086 |
| Kafka | PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094 | PLAINTEXT://kafka0:9092,PLAINTEXT://kafka1:9093,PLAINTEXT://kafka2:9094 |
| REST Proxy | [http://localhost:8082](http://localhost:8082/) | http://rest-proxy:8082/ |
| Schema Registry | [http://localhost:8081](http://localhost:8081/ ) | http://schema-registry:8081/ |
| Kafka Connect | [http://localhost:8083](http://localhost:8083) | http://kafka-connect:8083 |
| KSQL | [http://localhost:8088](http://localhost:8088) | http://ksql:8088 |
| PostgreSQL | `jdbc:postgresql://localhost:5432/cta` | `jdbc:postgresql://postgres:5432/cta` | `cta_admin` | `chicago` |

Note that to access these services from your own machine, you will always use the `Host URL` column.

When configuring services that run within Docker Compose, like **Kafka Connect you must use the Docker URL**. 

### Running the Simulation

There are two pieces to the simulation, the `producer` and `consumer`. 

#### To run the `producer`:

1. `cd producers`
2. `python -m venv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `python simulation.py`

Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

#### To run the Faust Stream Processing Application:
1. `cd consumers`
2. `python -m venv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `faust -A faust_stream worker -l info`


#### To run the KSQL Creation Script:
1. `cd consumers`
2. `python -m venv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `python ksql.py`

#### To run the `consumer`:

1. `cd consumers`
2. `python -m venv env`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `python server.py`

Once the server is running, you may hit `Ctrl+C` at any time to exit.
