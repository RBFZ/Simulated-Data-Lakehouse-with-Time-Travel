import pandas as pd
import os
from datetime import datetime

def evolve_schema(current_data_path='data/current_data.csv', historical_data_dir='data/historical_data'):
    if not os.path.exists(current_data_path):
        print(f"Error: {current_data_path} not found. Please run ingestion_script.py first.")
        return

    df = pd.read_csv(current_data_path)

    if 'Volume' not in df.columns:
        print("Adding 'Volume' column to the schema...")
        # Simulate adding a new column with some dummy data
        df["Volume"] = [100000 + i * 10000 for i in range(len(df))]
        
        # Save to current_data.csv with new schema
        df.to_csv(current_data_path, index=False)
        print(f"Schema evolved and data saved to {current_data_path}")

        # Save snapshot to historical_data directory after schema evolution
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        historical_file_path = os.path.join(historical_data_dir, f'{timestamp}_data_evolved.csv')
        df.to_csv(historical_file_path, index=False)
        print(f"Snapshot with evolved schema saved to {historical_file_path}")
    else:
        print("'Volume' column already exists. Schema not evolved.")

if __name__ == "__main__":
    evolve_schema()

