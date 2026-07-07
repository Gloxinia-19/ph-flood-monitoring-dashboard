import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

TABLE_NAME = "flood_events"
CLEANED_DATA_PATH = "data/processed/flood_events_cleaned.csv"

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env file.")

df = pd.read_csv(CLEANED_DATA_PATH)

engine = create_engine(DATABASE_URL)

with engine.begin() as connection:
    # Clear existing rows so running this script again does not duplicate data.
    connection.execute(text(f"TRUNCATE TABLE {TABLE_NAME} RESTART IDENTITY"))

    df.to_sql(
        TABLE_NAME,
        connection,
        if_exists="append",
        index=False
    )

print(f"Data loaded successfully into PostgreSQL table '{TABLE_NAME}'.")
