from connect_test.complex_type_schema_producer import TOPIC_NAME
from connect_test.connector import Connector


class ComplexSchemaConnector(Connector):
    """
    Creates a Kafka Connect Connector for the complex schema topic into Oracle
    """

    def __init__(self, base_endpoint):
        super().__init__(base_endpoint, TOPIC_NAME, "ComplexTypesOracleDatabaseDialect")
