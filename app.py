from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
from datetime import datetime

# Import our scripts
from ingestion_script import generate_stock_data, ingest_data
from schema_evolution_script import evolve_schema
from time_travel_script import get_data_as_of

app = Flask(__name__)

# Ensure data directories exist
if not os.path.exists("data/historical_data"):
    os.makedirs("data/historical_data")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/current_data")
def get_current_data():
    current_data_path = "data/current_data.csv"
    if os.path.exists(current_data_path):
        df = pd.read_csv(current_data_path)
        return jsonify(df.to_dict(orient="records"))
    return jsonify([])

@app.route("/api/historical_data")
def get_historical_data():
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Date parameter is missing."}), 400

    df, error = get_data_as_of(date_str)
    if error:
        return jsonify({"error": error}), 400
    
    if df is not None:
        return jsonify(df.to_dict(orient="records"))
    return jsonify([])

@app.route("/api/ingest_data", methods=["POST"])
def trigger_ingest_data():
    # Simulate new data coming in
    today = datetime.now().strftime("%Y-%m-%d")
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]
    prices = [152.0, 2510.0, 302.0, 125.0]
    new_df = generate_stock_data(today, stocks, prices)
    ingest_data(new_df)
    return jsonify({"message": "New data ingested successfully!"})

@app.route("/api/evolve_schema", methods=["POST"])
def trigger_evolve_schema():
    evolve_schema()
    return jsonify({"message": "Schema evolution triggered!"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

