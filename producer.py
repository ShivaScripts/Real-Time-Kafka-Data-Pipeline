from kafka import KafkaProducer
from faker import Faker
import json
import time
import logging
import random  # For generating random bursts

# Configure logging to write to a file
logging.basicConfig(filename='producer_log.txt', level=logging.INFO)

# Configure producer for high throughput
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks=0,  # No waiting for acknowledgment
    linger_ms=5,  # Batch messages for efficiency
    compression_type='gzip',  # Reduce data size
    batch_size=32768  # Increase batch size for fewer requests
)

fake = Faker()
TOPIC = "test-topic"


def generate_log():
    """Generate a fake log message with a random and skewed log level."""
    # Skewed probability distribution for log levels
    log_level = random.choices(
        ["INFO", "DEBUG", "ERROR"],
        weights=[50, 30, 20],  # INFO 50%, DEBUG 30%, ERROR 20%
        k=1
    )[0]
    return {
        "timestamp": time.time(),
        "level": log_level,
        "message": fake.sentence(),
        "service": fake.word()
    }


def generate_bursts():
    """Generate a burst of logs with varying counts for each log level."""
    # Randomly select a burst size between 100 and 1000 messages
    burst_size = random.randint(100, 1000)

    # Create a list of log entries with random levels
    burst = [generate_log() for _ in range(burst_size)]
    return burst


# Target: 278K messages per second (~1 billion per hour)
messages_per_batch = 5000
total_batches = 3600 * (278000 // messages_per_batch)  # 1-hour target

start_time = time.time()

for batch_num in range(total_batches):
    batch = []

    # Randomly decide the number of bursts per batch (1-5 bursts in each batch)
    burst_count = random.randint(1, 5)

    # Generate multiple bursts and add them to the batch
    for _ in range(burst_count):
        batch.extend(generate_bursts())  # Add the burst of messages

    # Send messages in the batch
    for msg in batch:
        producer.send(TOPIC, msg)
        logging.info(f"Sent message: {msg}")  # Log each sent message

    print(f"Batch sent: {batch_num + 1}/{total_batches}")  # Print batch progress
    time.sleep(0.01)

print("✅ 1 Billion messages scheduled for production!")

producer.flush()  # Ensure all messages are sent
