from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    group_id='email-service',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

print("Listening for messages...")
for message in consumer:
    print(f"Partition: {message.partition}, "
          f"Offset: {message.offset}, "
          f"Key: {message.key}, "
          f"Value: {message.value}")
