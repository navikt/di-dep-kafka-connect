from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from connect_test import config

"""
Produces messages with a flat Avro schema
"""

TOPIC_NAME = "complex_schema_test"

most_common_names_usa = [
    [1, "James", {"field1": "data", "field2": "data2"}],
    [2, "John", {"field1": "data", "field2": "data2"}],
    [3, "Robert", {"field1": "data", "field2": "data2"}],
    [4, "Michael", {"field1": "data", "field2": "data2"}],
    [5, "William", {"field1": "data", "field2": "data2"}],
    [6, "David", {"field1": "data", "field2": "data2"}],
    [7, "Richard", {"field1": "data", "field2": "data2"}],
    [8, "Joseph", {"field1": "data", "field2": "data2"}],
    [9, "Thomas", {"field1": "data", "field2": "data2"}],
    [10, "Charles", {"field1": "data", "field2": "data2"}],
]

value_schema_str = """
{
   "namespace": "test",
   "name": "complex_type_schema_test_value",
   "type": "record",
   "fields" : [
    {
        "name" : "rank",
        "type" : "int"
    },
    {
         "name": "name",
         "type": "string"
    },
    {
         "name": "data",
         "type": {
            "type": "record",
            "name": "innerdata",
            "fields" : [
                {
                    "name": "field1",
                    "type": "string"
                },
                {
                    "name": "field2",
                    "type": "string"
                }
            ]
     }
    
    }
   ]
}
"""

key_schema_str = """
{
   "namespace": "test",
   "name": "complex_type_schema_test_key",
   "type": "record",
   "fields" : [
     {
       "name" : "rank",
       "type" : "int"
     }
   ]
}
"""


def produce():
    value_schema = avro.loads(value_schema_str)
    key_schema = avro.loads(key_schema_str)

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    avro_producer = AvroProducer({
        'bootstrap.servers': config.BOOTSTRAP_SERVERS,
        'on_delivery': delivery_report,
        'schema.registry.url': config.SCHEMA_REGISTRY_URL
    }, default_key_schema=key_schema, default_value_schema=value_schema)

    cluster_metadata = avro_producer.list_topics()
    if TOPIC_NAME not in cluster_metadata.topics.keys():
        for name in most_common_names_usa:
            value = {"rank": name[0], "name": name[1], "data": name[2]}
            key = {"rank": name[0]}
            avro_producer.produce(topic=TOPIC_NAME, value=value, key=key)
        avro_producer.flush()
    else:
        print(f"{TOPIC_NAME} exists, do nothing")


if __name__ == '__main__':
    produce()
