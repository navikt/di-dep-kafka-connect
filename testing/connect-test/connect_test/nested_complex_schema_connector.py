from connect_test import config
from connect_test.connector import Connector
from connect_test.nested_complex_type_schema_producer import TOPIC_NAME

"""
Creates a Kafka Connect Connector for the nested complex schema topic into Oracle
"""

CONNECTOR_NAME = "Oracle_NestedComplexSchemaConnector"


def create():
    connector = Connector(config.CONNECT_REST_URL,
                          TOPIC_NAME,
                          CONNECTOR_NAME,
                          "ComplexTypesOracleDatabaseDialect",
                          "test_nested_complex"
                          )
    connector.create(verbose=True)


def get_connector_status():
    connector = Connector(config.CONNECT_REST_URL,
                          TOPIC_NAME,
                          CONNECTOR_NAME,
                          "ComplexTypesOracleDatabaseDialect",
                          "test_nested_complex"
                          )
    return connector.get_connector_status()


if __name__ == '__main__':
    create()
