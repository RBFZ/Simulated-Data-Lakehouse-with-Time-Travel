# Simulated-Data-Lakehouse-with-Time-Travel

## Project Overview

This project aims to demonstrate key concepts of a data product with features inspired by Apache Iceberg, specifically simplified schema evolution and time travel. It will involve a data ingestion script, a mechanism for managing data versions, and a web interface to visualize the data.

## Project Structure

```
. (project root)
├── data/
│   ├── current_data.csv
│   └── historical_data/
│       ├── 2025-06-10_data.csv
│       └── 2025-06-11_data.csv
├── ingestion_script.py
├── schema_evolution_script.py
├── time_travel_script.py
├── app.py (Flask backend)
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── README.md
```

## Data Model and Dataset Choice

For this project, we will use a simplified dataset representing daily stock prices. This dataset will allow us to easily demonstrate schema evolution (e.g., adding a new column like 'Volume') and time travel (viewing prices on a specific date).

**Initial Schema (e.g., `current_data.csv` on Day 1):**

| Date       | Stock  | Price |
|------------|--------|-------|
| 2025-06-10 | AAPL   | 150.0 |
| 2025-06-10 | GOOGL  | 2500.0|

**Evolved Schema (e.g., `current_data.csv` on Day X, after schema evolution):**

| Date       | Stock  | Price | Volume |
|------------|--------|-------|--------|
| 2025-06-XX | AAPL   | 155.0 | 100000 |
| 2025-06-XX | GOOGL  | 2550.0| 50000  |

## Data Storage Strategy

*   **`data/current_data.csv`**: This file will always hold the latest version of our data. The ingestion script will update this file.
*   **`data/historical_data/`**: This directory will store snapshots of `current_data.csv` at different points in time. Each snapshot will be named with a timestamp (e.g., `YYYY-MM-DD_data.csv`) to enable time travel.

## Schema Evolution Strategy

Schema evolution will be handled by modifying the ingestion script to introduce new columns. The Python Pandas library will be used to read and write CSV files, which can gracefully handle missing columns when reading older schemas and adding new ones when writing.

## Time Travel Strategy

Time travel will be implemented by allowing the user to specify a date. The backend API will then retrieve the corresponding historical data file from the `data/historical_data/` directory and serve it to the frontend.


### Features Demonstrated

1. **Data Ingestion**: The application can ingest new stock price data through the "Ingest New Data" button.

2. **Schema Evolution**: The application demonstrates schema evolution by adding a "Volume" column to the existing data structure through the "Evolve Schema (Add Volume)" button.

3. **Time Travel**: Users can query historical data by selecting a date and clicking "Load Data" (though the current implementation shows current data for today's date).

4. **Web Interface**: A clean, responsive web interface that displays current data and provides controls for data ingestion, schema evolution, and time travel.

### Technical Implementation

- **Backend**: Flask application with RESTful API endpoints
- **Frontend**: HTML, CSS, and JavaScript with responsive design
- **Data Storage**: CSV files with timestamped snapshots for historical data
- **Schema Management**: Pandas-based data manipulation with graceful handling of schema changes

This project successfully demonstrates the core concepts of Apache Iceberg (schema evolution and time travel) in a simplified, educational format suitable for a resume project.

