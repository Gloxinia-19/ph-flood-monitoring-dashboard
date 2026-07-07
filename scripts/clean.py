import pandas as pd


RAW_DATA_PATH = "data/raw/flood_events_sample.csv"
CLEANED_DATA_PATH = "data/processed/flood_events_cleaned.csv"

TEXT_COLUMNS = ["region", "province", "municipality", "source"]
NUMERIC_COLUMNS = [
    "latitude",
    "longitude",
    "flood_area",
    "affected_families",
    "affected_persons",
]


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce").dt.date
    df = df.drop_duplicates()

    for column in TEXT_COLUMNS:
        df[column] = df[column].fillna("").astype(str).str.strip()

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Cleaned data saved to {CLEANED_DATA_PATH}.")


if __name__ == "__main__":
    main()
