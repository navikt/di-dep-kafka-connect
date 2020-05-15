import time

import pytest
from connect_test import complex_type_schema_producer, \
    flat_schema_producer, \
    nested_complex_type_schema_producer
from connect_test.complex_schema_connector import ComplexSchemaConnector
from connect_test.compose import Compose
from connect_test.flat_schema_connector import FlatSchemaConnector
from connect_test.nested_complex_schema_connector import NestedComplexSchemaConnector


class TestKafkaConnect():
    @pytest.fixture(scope="module", autouse=True)
    def rest_api(self):
        c = Compose()
        try:
            yield c.up()
        finally:
            c.down()

    @pytest.fixture(scope="class", autouse=True)
    def produce(self):
        complex_type_schema_producer.produce()
        flat_schema_producer.produce()
        nested_complex_type_schema_producer.produce()

    def test_create_flat_schema_connector(self, rest_api):
        connector = FlatSchemaConnector(rest_api)
        connector.create()
        time.sleep(2)
        connector_status = connector.get_connector_status()
        assert "RUNNING" == connector_status["connector"]["state"]
        for task in connector_status["tasks"]:
            assert "RUNNING" == task["state"]

    def test_create_complex_schema_connector(self, rest_api):
        connector = ComplexSchemaConnector(rest_api)
        connector.create()  # should not throw exception
        time.sleep(2)
        connector_status = connector.get_connector_status()
        assert "RUNNING" == connector_status["connector"]["state"]
        for task in connector_status["tasks"]:
            assert "RUNNING" == task["state"]

    def test_nested_create_complex_schema_connector(self, rest_api):
        connector = NestedComplexSchemaConnector(rest_api)
        connector.create()  # should not throw exception
        time.sleep(2)
        connector_status = connector.get_connector_status()
        assert "RUNNING" == connector_status["connector"]["state"]
        for task in connector_status["tasks"]:
            assert "RUNNING" == task["state"]


