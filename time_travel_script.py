import pandas as pd
import os
from datetime import datetime

def get_data_as_of(date_str, historical_data_dir='data/historical_data', current_data_path='data/current_data.csv'):
    """ 
    Retrieves data as of a specific date.
    If the date is today, it returns current_data.csv.
    Otherwise, it looks for the closest snapshot in historical_data before or on that date.
    """
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None, "Invalid date format. Please use YYYY-MM-DD."

    today = datetime.now().date()

    if target_date >= today:
        if os.path.exists(current_data_path):
            print(f"Returning current data from {current_data_path}")
            return pd.read_csv(current_data_path), None
        else:
            return None, f"Current data file not found: {current_data_path}"

    available_snapshots = []
    for filename in os.listdir(historical_data_dir):
        if filename.endswith(".csv"):
            try:
                # Extract date from filenames like YYYY-MM-DD_HH-MM-SS_data.csv or YYYY-MM-DD_HH-MM-SS_data_evolved.csv
                file_date_str = filename.split("_")[:3]
                file_date_str = "-".join(file_date_str)
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
                if file_date <= target_date:
                    available_snapshots.append((file_date, filename))
            except ValueError:
                print(f"Could not parse date from filename: {filename}")
                continue
    
    if not available_snapshots:
        return None, f"No historical data found on or before {date_str}."

    # Find the closest snapshot to the target date
    available_snapshots.sort(key=lambda x: x[0], reverse=True)
    closest_snapshot_date, closest_snapshot_file = available_snapshots[0]
    
    snapshot_path = os.path.join(historical_data_dir, closest_snapshot_file)
    print(f"Returning historical data from {snapshot_path} (snapshot date: {closest_snapshot_date})")
    return pd.read_csv(snapshot_path), None

if __name__ == "__main__":
    # Example usage:
    # Make sure you have run ingestion_script.py first to create some data.
    # And optionally schema_evolution_script.py to have an evolved schema snapshot.

    # Test 1: Get current data (assuming today is 2025-06-10 or later)
    df_current, err = get_data_as_of(datetime.now().strftime("%Y-%m-%d"))
    if err:
        print(f"Error: {err}")
    elif df_current is not None:
        print("\nCurrent Data:")
        print(df_current.to_string())

    # Test 2: Get data from a past date (e.g., yesterday or the day of the first ingestion)
    # Adjust this date based on when you ran ingestion_script.py
    # For this example, we assume ingestion_script.py was run on 2025-06-10
    df_past, err = get_data_as_of("2025-06-10") 
    if err:
        print(f"Error: {err}")
    elif df_past is not None:
        print("\nPast Data (2025-06-10 or earliest available before that):")
        print(df_past.to_string())

    # Test 3: Get data from a date with no snapshot (should return closest previous or error)
    df_no_exact_snapshot, err = get_data_as_of("2025-01-01")
    if err:
        print(f"\nError for 2025-01-01: {err}")
    elif df_no_exact_snapshot is not None:
        print("\nData for 2025-01-01 (or closest before):")
        print(df_no_exact_snapshot.to_string())

