# Local test setup

This brings up Kafka with Connect and the nginx proxy for local testing.

## Using

Run `docker-compose up`. The command might fail because zookeeper uses longer time to start than kafka, so you might have to run `docker-compose up -d kafka` after a while if it exits.

## Endpoints

| Name          | Adress         |
| ---           | -----          |
| Kafka Connect | localhost:8084 |
| Nginx proxy   | localhost:8083 |

To find the ports for the other services run `docker ps`.

## Authentication

The local password and username for the nginx proxy is `test`.

## Helper scripts

Dagpenger has a nice [collection of scripts](https://github.com/navikt/dagpenger/tree/master/script) for communicating with Kafka.
