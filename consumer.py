from kafka import KafkaConsumer
import json

# Initialize KafkaConsumer
consumer = KafkaConsumer(
    "test-topic",  # Topic name
    bootstrap_servers="localhost:9092",  # Kafka server
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # Deserialize messages from JSON format
    enable_auto_commit=True,
    fetch_max_bytes=10485760,  # Maximum fetch size (10MB)
    max_partition_fetch_bytes=2097152,  # Max fetch per partition (2MB)
)

count = 0

# Open a file to store consumed messages (appending data)
with open('/Users/Shivam/Documents/real_time_pipeline/consumed_data.json', 'a') as file:
    print("Consumer is starting...")  # Add starting log
    for message in consumer:
        print(f"Received message: {message.value}")  # Print each message
        count += 1
        data = message.value  # Get the message content

        # Write the consumed message to the file as a JSON object
        file.write(json.dumps(data) + "\n")

        # Print progress every 100K messages
        if count % 100000 == 0:
            print(f"✅ Consumed {count} messages...")

        # Stop after consuming a certain number of messages (for example, 1 million)
        if count >= 10000000:
            break

print(f"✅ Finished consuming {count} messages.")
