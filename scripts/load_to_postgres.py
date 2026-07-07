import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env file.")

df = pd.read_csv("data/raw/flood_events_sample.csv")

engine = create_engine(DATABASE_URL)

df.to_sql(
    "flood_events",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully into PostgreSQL.")
