import pytest
import time

from connect_test import complex_type_schema_producer, \
    flat_schema_producer, \
    complex_schema_connector, \
    flat_schema_connector, \
    nested_complex_schema_connector, \
    nested_complex_type_schema_producer


class TestKafkaConnect():
    @pytest.fixture(scope="class", autouse=True)
    def produce(self):
        complex_type_schema_producer.produce()
        flat_schema_producer.produce()
        nested_complex_type_schema_producer.produce()

    def test_create_flat_schema_connector(self):
        flat_schema_connector.create()  # should not throw exception
        time.sleep(2)
        connector_status = flat_schema_connector.get_connector_status()
        assert "RUNNING" == connector_status["connector"]["state"]
        for task in connector_status["tasks"]:
            assert "RUNNING" == task["state"]

    def test_create_complex_schema_connector(self):
        complex_schema_connector.create()  # should not throw exception
        time.sleep(2)
        connector_status = complex_schema_connector.get_connector_status()
        assert "RUNNING" == connector_status["connector"]["state"]
        for task in connector_status["tasks"]:
            assert "RUNNING" == task["state"]

    def test_nested_create_complex_schema_connector(self):
        nested_complex_schema_connector.create()  # should not throw exception
        time.sleep(2)
        connector_status = nested_complex_schema_connector.get_connector_status()
        assert "RUNNING" == connector_status["connector"]["state"]
        for task in connector_status["tasks"]:
            assert "RUNNING" == task["state"]


