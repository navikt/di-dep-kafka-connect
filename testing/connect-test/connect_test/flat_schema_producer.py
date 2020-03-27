from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from connect_test import config

"""
Produces messages with a flat Avro schema
"""

TOPIC_NAME = "flat_schema_test"

most_common_names_usa = [
    [1, "James", 4764644],
    [2, "John", 4546819],
    [3, "Robert", 4535897],
    [4, "Michael", 4323074],
    [5, "William", 3631876],
    [6, "David", 3560660],
    [7, "Richard", 2477879],
    [8, "Joseph", 2367801],
    [9, "Thomas", 2167014],
    [10, "Charles", 2124748],
]

value_schema_str = """
{
   "namespace": "test",
   "name": "flat_schema_test_value",
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
         "name": "number",
         "type": "int"
     }
   ]
}
"""

key_schema_str = """
{
   "namespace": "test",
   "name": "flat_schema_test_key",
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

    avroProducer = AvroProducer({
        'bootstrap.servers': config.BOOTSTRAP_SERVERS,
        'on_delivery': delivery_report,
        'schema.registry.url': config.SCHEMA_REGISTRY_URL
    }, default_key_schema=key_schema, default_value_schema=value_schema)

    cluster_metadata = avroProducer.list_topics()
    if TOPIC_NAME not in cluster_metadata.topics.keys():
        # Create topic and produce message if it does not exist
        for name in most_common_names_usa:
            value = {"rank": name[0], "name": name[1], "number": name[2]}
            key = {"rank": name[0]}
            avroProducer.produce(topic=TOPIC_NAME, value=value, key=key)
        avroProducer.flush()
    else:
        print(f"Topic={TOPIC_NAME} exists, do nothing")


if __name__ == "__main__":
    produce()
