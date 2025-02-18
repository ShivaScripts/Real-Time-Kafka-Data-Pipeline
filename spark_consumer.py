import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import time
import pandas as pd
from kafka import KafkaConsumer

# Kafka Consumer Setup
TOPIC = "fake-logs"
BOOTSTRAP_SERVERS = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode("utf-8"),
)

# Dash App Setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time Kafka Data Visualization"),
    dcc.Graph(id="live-graph"),
    dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
])

# Store incoming data
data_records = []

# Function to constantly consume data
def consume_data():
    global data_records
    for message in consumer:
        timestamp = time.strftime("%H:%M:%S")
        data_records.append({"time": timestamp, "message": message.value})
        if len(data_records) > 50:
            data_records.pop(0)

threading.Thread(target=consume_data, daemon=True).start()

@app.callback(
    Output("live-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_graph(n):
    df = pd.DataFrame(data_records)
    if df.empty:
        return go.Figure()

    return {
        "data": [go.Scatter(x=df["time"], y=df.index, mode="lines+markers")],
        "layout": go.Layout(title="Incoming Messages", xaxis={"title": "Time"}, yaxis={"title": "Message Count"})
    }

if __name__ == "__main__":
    app.run_server(debug=True)
