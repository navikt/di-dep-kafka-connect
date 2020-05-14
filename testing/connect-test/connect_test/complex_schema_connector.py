from connect_test import config
from connect_test.complex_type_schema_producer import TOPIC_NAME
from connect_test.connector import Connector

"""
Creates a Kafka Connect Connector for the flat schema topic into Oracle
"""

CONNECTOR_NAME = "Oracle_ComplexSchemaConnector"


def create():
    connector = Connector(config.CONNECT_REST_URL, TOPIC_NAME, CONNECTOR_NAME, "ComplexTypesOracleDatabaseDialect")
    connector.create(verbose=True)


def get_connector_status():
    connector = Connector(config.CONNECT_REST_URL, TOPIC_NAME, CONNECTOR_NAME, "ComplexTypesOracleDatabaseDialect")
    return connector.get_connector_status()


if __name__ == '__main__':
    create()
