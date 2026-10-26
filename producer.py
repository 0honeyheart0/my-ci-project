from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

for i in range(10):
    message = {
        'order_id': i,
        'user': f'user-{i % 3}',
        'amount': (i + 1) * 100
    }
    producer.send('orders', key=f'user-{i % 3}', value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
producer.close()
print("Done.")
