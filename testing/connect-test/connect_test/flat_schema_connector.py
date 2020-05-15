from connect_test.connector import Connector
from connect_test.flat_schema_producer import TOPIC_NAME


class FlatSchemaConnector(Connector):
    """
    Creates a Kafka Connect Connector for the flat schema topic into Oracle
    """

    def __init__(self, base_endpoint):
        super().__init__(base_endpoint, TOPIC_NAME)
