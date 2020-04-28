# NADA Kafka Connect NAIS deployment prerequisites

1. To deploy a new NADA Kafka Connect cluster to NAIS the Connect topics need to be created.

- <prefix>-config
- <prefix>-offsets
- <prefix>-status

2. To create Connectors that can connect to Kafka topics in NAV a service-user that can be granted access to the topics needs to be created. 



## Create Connect topics

### Using Kafka Admin REST

Topic management in NAV IT is done through the Middleman "Kafka Admin REST". To create, update and delete topics [Kafka Admin REST](https://github.com/navikt/kafka-adminrest) is used.

1. Access the correct application instance for the 

