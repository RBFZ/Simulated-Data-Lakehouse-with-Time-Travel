
import pandas as pd
import os
from datetime import datetime

def generate_stock_data(date, stocks, prices, volumes=None):
    data = {
        'Date': [date] * len(stocks),
        'Stock': stocks,
        'Price': prices
    }
    if volumes:
        data['Volume'] = volumes
    return pd.DataFrame(data)

def ingest_data(df, current_data_path='data/current_data.csv', historical_data_dir='data/historical_data'):
    # Save to current_data.csv
    df.to_csv(current_data_path, index=False)
    print(f"Data saved to {current_data_path}")

    # Save snapshot to historical_data directory
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    historical_file_path = os.path.join(historical_data_dir, f'{timestamp}_data.csv')
    df.to_csv(historical_file_path, index=False)
    print(f"Snapshot saved to {historical_file_path}")

if __name__ == "__main__":
    # Initial data ingestion
    today = datetime.now().strftime('%Y-%m-%d')
    stocks = ['AAPL', 'GOOGL', 'MSFT']
    prices = [150.0, 2500.0, 300.0]
    initial_df = generate_stock_data(today, stocks, prices)
    ingest_data(initial_df)

    # Simulate schema evolution later by adding 'Volume' column
    # For now, this script only handles initial data and snapshots


