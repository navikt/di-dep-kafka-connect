from connect_test.connector import Connector
from connect_test.nested_complex_type_schema_producer import TOPIC_NAME


class NestedComplexSchemaConnector(Connector):
    """
    Creates a Kafka Connect Connector for the nested complex schema topic into Oracle
    """

    def __init__(self, base_endpoint):
        super().__init__(base_endpoint,
                         TOPIC_NAME,
                         "ComplexTypesOracleDatabaseDialect",
                         "test_nested_complex")
