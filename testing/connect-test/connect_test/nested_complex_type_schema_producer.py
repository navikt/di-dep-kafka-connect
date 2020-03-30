import json

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from connect_test import config

"""
Produces messages with a data field with a nested complex structure Avro schema. Reasoning: Test the Struct to Json 
support.
"""

TOPIC_NAME = "nested_complex_schema_test"


data = [
    {"rank": 1, "name": "James", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 2, "name": "John", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 3, "name": "Robert", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 4, "name": "Michael", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 5, "name": "William", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 6, "name": "David", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 7, "name": "Richard", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 8, "name": "James", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 9, "name": "Joseph", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
    {"rank": 10, "name": "Charles", "data": {"field1": {"nested": {"even_more_nested": 1.234, "another_field": 2}}, "field2": "data2"}},
]

value_schema_dict = {
  "name": "nested_complex_value_schema",
  "type": "record",
  "namespace": "com.acme.avro",
  "fields": [
    {
      "name": "rank",
      "type": "int"
    },
    {
      "name": "name",
      "type": "string"
    },
    {
      "name": "data",
      "type": {
        "name": "data",
        "type": "record",
        "fields": [
          {
            "name": "field1",
            "type": {
              "name": "field1",
              "type": "record",
              "fields": [
                {
                  "name": "nested",
                  "type": {
                    "name": "nested",
                    "type": "record",
                    "fields": [
                      {
                        "name": "even_more_nested",
                        "type": "double"
                      },
                      {
                        "name": "another_field",
                        "type": "int"
                      }
                    ]
                  }
                }
              ]
            }
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


key_schema_dict = {
   "namespace": "test",
   "name": "nested_complex_type_schema_test_key",
   "type": "record",
   "fields" : [
     {
       "name" : "rank",
       "type" : "int"
     }
   ]
}


def produce():
    value_schema = avro.loads(json.dumps(value_schema_dict))
    key_schema = avro.loads(json.dumps(key_schema_dict))

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
        for value in data:
            key = {"rank": value["rank"]}
            avro_producer.produce(topic=TOPIC_NAME, value=value, key=key)
        avro_producer.flush()
    else:
        print(f"{TOPIC_NAME} exists, do nothing")


if __name__ == '__main__':
    produce()
