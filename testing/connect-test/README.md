# Simple Dumb Test closet (not suite ;) ) for NADA Kafka Connect setup

## What it does

### Creates test topics with schema and test data

- Flat schema
- Complex schema

### Creates Connectors using the test topics

- Flat schema data to Oracle
- Complex schema data to Oracle

### Checks that the Connectors end up with status=RUNNING

NOTE: Currently the complex schema fails!

## What it requires

That Kafka, Kafka Connect, schema registry and the databases that are used (currently only Oracle) are available. The docker-compose.yml sets up the required environment. The tests are meant to be ran from the local host not from within a docker container in the compose network.
