# Real-Time Kafka Data Pipeline: Simulating 1 Billion Messages per Hour

## 📜 Project Description

This project simulates a high-throughput real-time data pipeline using Kafka, where log messages are produced and consumed at a rate of approximately **1 billion messages per hour**. The pipeline consists of:

- A **Kafka producer** that generates random log messages with varying levels (`INFO`, `DEBUG`, `ERROR`).
- A **Kafka consumer** that consumes these messages and stores them in JSON format.
- A **Spark consumer** that processes the messages for transformation.
- A **dynamic dashboard** powered by Dash and Plotly, visualizing real-time message counts by log level.

The pipeline is designed to handle and simulate massive amounts of data while providing real-time insights into the generated log data.
## 🎥 Demo

### Consumer consuming ~100k messages/hr
![Consumer consuming ~100k messages/min ](https://github.com/ShivaScripts/assets/raw/main/Final2.gif)

### Dashboard Visualizing ~100k messages/hr in real-time
![Dashboard Visualizing ~100k messages/hr in real-time](https://github.com/ShivaScripts/assets/raw/main/VID-20250218-WA0020.gif)

### Producer producing message in real-time
![Producer producing message in real-time](https://github.com/ShivaScripts/assets/raw/main/VID-20250218-WA0007.gif)
## Run Locally

To run the project locally on your machine, follow the steps below:

### Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.x**: You can download it from [here](https://www.python.org/downloads/).
- **Kafka**: You can follow the [Kafka Quickstart Guide](https://kafka.apache.org/quickstart) to install and run Apache Kafka locally.
- **Zookeeper**: Kafka requires Zookeeper to be running. Zookeeper is bundled with Kafka, so you can start it from Kafka's `bin/` folder.
- **Spark (Optional for transformation)**: If you want to use the Spark consumer for data transformation, you’ll need to install Apache Spark.

### Steps to Run

1. **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-folder>
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Mac/Linux
    venv\Scripts\activate     # For Windows
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Start Kafka and Zookeeper**:

    - **Start Zookeeper** (in a separate terminal window):
      ```bash
      ./bin/zookeeper-server-start.sh config/zookeeper.properties
      ```

    - **Start Kafka** (in another terminal window):
      ```bash
      ./bin/kafka-server-start.sh config/server.properties
      ```

5. **Run the Producer**:
    In a separate terminal window, run the Kafka producer to start sending messages:
    ```bash
    python producer.py
    ```

6. **Run the Consumer**:
    In a separate terminal window, run the Kafka consumer to consume the messages:
    ```bash
    python consumer.py
    ```

7. **Run the Spark Consumer** (Optional for transformation):
    If you want to process the messages using Spark, run the Spark consumer:
    ```bash
    python spark_consumer.py
    ```

8. **Run the Dashboard**:
    In a separate terminal window, start the dashboard server:
    ```bash
    python dashboard.py
    ```

    Once the server is running, open your browser and go to `http://127.0.0.1:8050/` to view the real-time Kafka data visualization dashboard.

### Note
- Make sure Kafka and Zookeeper are running before starting the producer and consumer.
- The dashboard will visualize real-time data as it is consumed from Kafka and processed by Spark.
## 🔥 Real-Time Data Streaming with Kafka & Spark  

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)  
![Kafka](https://img.shields.io/badge/Apache%20Kafka-Streaming-red?style=for-the-badge&logo=apachekafka)  
![Spark](https://img.shields.io/badge/Apache%20Spark-Streaming-orange?style=for-the-badge&logo=apachespark)  
![Real-Time Processing](https://img.shields.io/badge/Real--Time%20Processing-1B%20msgs/hr-green?style=for-the-badge)  
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)  
