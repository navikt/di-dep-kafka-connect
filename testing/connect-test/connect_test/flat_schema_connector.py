from connect_test import config
from connect_test.connector import Connector
from connect_test.flat_schema_producer import TOPIC_NAME

"""
Creates a Kafka Connect Connector for the flat schema topic into Oracle
"""

CONNECTOR_NAME = "Oracle_FlatSchemaConnector"


def create():
    connector = Connector(config.CONNECT_REST_URL, TOPIC_NAME, CONNECTOR_NAME)
    connector.create(verbose=True)


def get_connector_status():
    connector = Connector(config.CONNECT_REST_URL, TOPIC_NAME, CONNECTOR_NAME)
    return connector.get_connector_status()


if __name__ == '__main__':
    create()
    get_connector_status()
