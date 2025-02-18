import time
import threading
import pandas as pd
from kafka import KafkaConsumer
import json
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Kafka Consumer Setup
TOPIC = "test-topic"
BOOTSTRAP_SERVERS = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),  # Deserialize as JSON
)

# Dash App Setup
app = dash.Dash(__name__)

# Layout with custom CSS styling
app.layout = html.Div(
    children=[
        html.Div(
            children=[html.H1("Real-Time Kafka Data Visualization", style={"textAlign": "center", "color": "#007bff"})],
            style={"marginBottom": "50px"}
        ),
        dcc.Graph(id="live-graph"),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
    ],
    style={"backgroundColor": "#f4f4f9", "height": "100vh", "display": "flex", "flexDirection": "column",
           "alignItems": "center", "justifyContent": "center"},
)

# Store incoming data
data_records = []

# Function to consume data from Kafka
def consume_data():
    global data_records
    start_time = time.time()  # Track start time
    for message in consumer:
        data = message.value
        timestamp = time.strftime("%H:%M:%S")
        level = data.get("level", "INFO")

        data_records.append({"time": timestamp, "level": level})

        # Reset after 60 seconds (1 minute)
        if time.time() - start_time >= 60:
            data_records = []  # Reset the data records
            start_time = time.time()  # Restart the timer

# Start the Kafka consumer in a separate thread
threading.Thread(target=consume_data, daemon=True).start()

@app.callback(
    Output("live-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_graph(n):
    # Convert the data_records to a DataFrame
    df = pd.DataFrame(data_records)

    if df.empty:
        return go.Figure()

    # Count the number of messages per log level for the graph
    level_counts = df["level"].value_counts()

    # Create a bar chart for each log level as a separate trace
    traces = []
    colors = {"INFO": "#4caf50", "DEBUG": "#2196f3", "ERROR": "#f44336"}

    for level in level_counts.index:
        traces.append(
            go.Bar(
                x=[level],
                y=[level_counts[level]],
                name=level,
                marker=dict(color=colors.get(level, "#888")),
                opacity=0.8,
            )
        )

    # Create the graph with dynamic features
    return {
        "data": traces,
        "layout": go.Layout(
            title="Real-Time Message Count by Level",
            xaxis={
                "title": "Log Level",
                "showgrid": False,
                "tickangle": 45,
                "ticks": "outside",
                "tickwidth": 2,
            },
            yaxis={
                "title": "Count",
                "showgrid": True,
                "gridwidth": 0.5,
                "zeroline": False,
            },
            paper_bgcolor="#f4f4f9",
            plot_bgcolor="#f4f4f9",
            font={"family": "Arial", "size": 14, "color": "#333"},
            transition={"duration": 500, "easing": "cubic-in-out"},
            hovermode="closest",
            barmode="stack",  # Stack bars for each log level
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True)
