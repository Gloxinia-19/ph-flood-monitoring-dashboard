# Philippines Flood Data Pipeline and Dashboard

A beginner-friendly data engineering and visualization project for Philippine flood events. The project uses PostgreSQL for storage, Python for ETL, and Streamlit with Plotly for an interactive dashboard.

The included data is sample data for portfolio and learning purposes. It is labeled in the `source` column.

## Tech Stack

- PostgreSQL
- Docker Compose
- Python
- pandas
- SQLAlchemy
- Streamlit
- Plotly

## Pipeline Flow

1. Store sample flood events in `data/raw/flood_events_sample.csv`.
2. Clean the raw CSV with `scripts/clean.py`.
3. Save cleaned data to `data/processed/flood_events_cleaned.csv`.
4. Load cleaned data into PostgreSQL with `scripts/load_to_postgres.py`.
5. Visualize the PostgreSQL table in `dashboard/app.py`.

## Folder Structure

```text
ph-flood-monitoring-dashboard/
├── data/
│   ├── raw/
│   │   └── flood_events_sample.csv
│   └── processed/
│       └── flood_events_cleaned.csv
├── scripts/
│   ├── extract.py
│   ├── clean.py
│   └── load_to_postgres.py
├── sql/
│   └── create_tables.sql
├── dashboard/
│   └── app.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How to Run in Codespaces

Start PostgreSQL:

```bash
docker compose up -d
```

Create your local environment file:

```bash
cp .env.example .env
```

Install Python packages:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL table:

```bash
docker exec -i ph_flood_postgres psql -U postgres -d ph_flood_db < sql/create_tables.sql
```

Clean the sample data:

```bash
python scripts/clean.py
```

Load the cleaned data into PostgreSQL:

```bash
python scripts/load_to_postgres.py
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Dashboard Features

- Sidebar filters for region, province, and date range
- KPI cards for total flood events, affected families, affected persons, and flood area
- Bar chart of flood events by region
- Bar chart of top affected provinces by affected persons
- Line chart of flood events over time
- Map of flood event locations
- Filtered flood event data table

## Future Improvements

- Replace sample data with an official public dataset.
- Add scheduled data extraction from a reliable source.
- Add data validation tests.
- Add more geographic layers for provinces and regions.
- Deploy the dashboard to a public hosting platform.
