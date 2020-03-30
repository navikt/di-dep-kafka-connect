import requests
import json

from connect_test import config
from connect_test.nested_complex_type_schema_producer import TOPIC_NAME

"""
Creates a Kafka Connect Connector for the nested complex schema topic into Oracle
"""

CONNECTOR_NAME = "Oracle_NestedComplexSchemaConnector"
HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

def create():
    endpoint = config.CONNECT_REST_URL + "/connectors"
    connector_config = {
        "name": CONNECTOR_NAME,
        "config": {
            "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
            "connection.password": "oracle",
            "topics": TOPIC_NAME,
            "tasks.max": "1",
            "connection.user": "system",
            "auto.create": "true",
            "connection.url": "jdbc:oracle:thin:@oracle:1521:xe",
            "insert.mode": "insert",
            "pk.mode": "record_key",
            "table.name.format": "test_nested_complex",
            "dialect.name": "ComplexTypesOracleDatabaseDialect",
        }
    }

    connectors = requests.get(endpoint, headers=HEADERS)
    if CONNECTOR_NAME not in connectors.json():
        response = requests.post(endpoint, json=connector_config, headers=HEADERS)
        print(response.text)
    else:
        print(f"Connector={CONNECTOR_NAME} exists, do nothing")


def get_connector_status():
    endpoint = config.CONNECT_REST_URL + f"/connectors/{CONNECTOR_NAME}/status"
    connector_metadata = requests.get(endpoint, headers=HEADERS)
    return connector_metadata.json()


if __name__ == '__main__':
    create()