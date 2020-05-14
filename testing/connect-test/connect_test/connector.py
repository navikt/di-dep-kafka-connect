from urllib.parse import urljoin

import requests


HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}


class Connector(object):
    def __init__(self, base_endpoint, topic_name, connector_name, dialect=None, table_name=None):
        self.base_endpoint = base_endpoint
        self.connector_name = connector_name
        self.topic_name = topic_name
        self.dialect = dialect
        self.table_name = table_name
        config = {
            "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
            "connection.password": "${vault:secret/oracle/local:password}",
            "topics": self.topic_name,
            "tasks.max": "1",
            "connection.user": "system",
            "auto.create": "true",
            "connection.url": "jdbc:oracle:thin:@oracle:1521:xe",
            "insert.mode": "insert",
            "pk.mode": "record_key",
            "table.name.format": "test_${topic}",
        }
        if table_name:
            config["table.name.format"] = table_name
        if dialect:
            config["dialect.name"] = dialect
        self._connector_config = {
            "name": self.connector_name,
            "config": config
        }

    def create(self, verbose=False):
        endpoint = urljoin(self.base_endpoint, "connectors")
        resp = requests.get(endpoint, headers=HEADERS)
        if self.connector_name not in resp.json():
            response = requests.post(endpoint, json=self._connector_config, headers=HEADERS)
            if verbose:
                print(response.text)
        else:
            if verbose:
                print(f"Connector={self.connector_name} exists, do nothing")

    def get_connector_status(self):
        endpoint = urljoin(self.base_endpoint, f"connectors/{self.connector_name}/status")
        connector_metadata = requests.get(endpoint, headers=HEADERS)
        return connector_metadata.json()
