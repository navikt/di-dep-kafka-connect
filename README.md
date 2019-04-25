# Data og Innsikt - Kafka Connect

Docker Kafka Connect image for deployment on [NAIS](https://nais.io/) based on [cp-kafka-connect](https://hub.docker.com/r/confluentinc/cp-kafka-connect/).

## Usage

### Prerequisites

Kafka Connect needs [three topics](https://docs.confluent.io/current/connect/userguide.html#distributed-mode) to run in distributed mode.

The prefix can be adjusted by setting the env variable `KAFKA_TOPIC_PREFIX` which by default is set to `di-dep-connect`. The suffixes are `offsets`, `configs`, `status`.

With some modifications to the topic name the [navikt/di-connect/init_topics.sh](https://github.com/navikt/di-connect/blob/master/init_topics.sh) script can be used to create the topics by running requests toward `kafka-adminrest`.

### ENV variables

In addition to the [required variables](https://docs.confluent.io/current/installation/docker/config-reference.html#kafka-connect-configuration)
we also need to configure SASL_SSL to be able to access the internal cluster using the right environment variables:

- `CONNECT_[(CONSUMER/PRODUCER)]_SSL_TRUSTSTORE_LOCATION`
- `CONNECT_[(CONSUMER/PRODUCER)]_SSL_TRUSTSTORE_PASSWORD`
- `CONNECT_[(CONSUMER/PRODUCER)]_SASL_JAAS_CONFIG`

Configuration of all environment variables not defined in [nais.yaml](nais.yaml) is handled through Vault or NAV specific environment variables in [run.sh](run.sh).

Vault -> ENV var mapping:

| Environment variable      | Vault key         |
| ----                      | ------            |
| *_SCHEMA_REGISTRY_URL     | schema.registry   |
| *_SASL_JAAS_CONFIG        | sasl.jaas.config  |
| CONNECT_BOOTSTRAP_SERVERS | bootstrap.servers |
