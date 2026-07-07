import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


st.set_page_config(
    page_title="Philippines Flood Monitoring Dashboard",
    page_icon="PH",
    layout="wide",
)

load_dotenv()


@st.cache_data(ttl=60)
def load_flood_data():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is missing. Create .env from .env.example first.")

    engine = create_engine(database_url)

    query = text(
        """
        SELECT
            event_id,
            event_date,
            region,
            province,
            municipality,
            latitude,
            longitude,
            flood_area,
            affected_families,
            affected_persons,
            source,
            created_at
        FROM flood_events
        ORDER BY event_date, region, province, municipality
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


st.title("Philippines Flood Monitoring Dashboard")

try:
    df = load_flood_data()
except (SQLAlchemyError, ValueError) as error:
    st.error(
        "Unable to load flood data from PostgreSQL. Make sure the database is running "
        "and the table has been created and loaded."
    )
    st.code(
        "docker compose up -d\n"
        "cp .env.example .env\n"
        "pip install -r requirements.txt\n"
        "docker exec -i ph_flood_postgres psql -U postgres -d ph_flood_db < sql/create_tables.sql\n"
        "python scripts/clean.py\n"
        "python scripts/load_to_postgres.py"
    )
    st.caption(f"Details: {error}")
    st.stop()

if df.empty:
    st.warning("No flood events found. Run the clean and load scripts to add sample data.")
    st.stop()

df["event_date"] = pd.to_datetime(df["event_date"])

st.sidebar.header("Filters")

regions = sorted(df["region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

province_options = sorted(df[df["region"].isin(selected_regions)]["province"].dropna().unique())
selected_provinces = st.sidebar.multiselect(
    "Province",
    province_options,
    default=province_options,
)

min_date = df["event_date"].min().date()
max_date = df["event_date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered_df = df[
    df["region"].isin(selected_regions)
    & df["province"].isin(selected_provinces)
    & (df["event_date"].dt.date >= start_date)
    & (df["event_date"].dt.date <= end_date)
]

total_events = len(filtered_df)
total_families = int(filtered_df["affected_families"].sum())
total_persons = int(filtered_df["affected_persons"].sum())
total_area = float(filtered_df["flood_area"].sum())

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric("Total flood events", f"{total_events:,}")
kpi_2.metric("Total affected families", f"{total_families:,}")
kpi_3.metric("Total affected persons", f"{total_persons:,}")
kpi_4.metric("Total flood area", f"{total_area:,.1f}")

if filtered_df.empty:
    st.info("No records match the selected filters.")
    st.stop()

left_chart, right_chart = st.columns(2)

events_by_region = (
    filtered_df.groupby("region", as_index=False)
    .size()
    .rename(columns={"size": "flood_events"})
    .sort_values("flood_events", ascending=False)
)

fig_region = px.bar(
    events_by_region,
    x="region",
    y="flood_events",
    title="Flood Events by Region",
    labels={"region": "Region", "flood_events": "Flood events"},
)
left_chart.plotly_chart(fig_region, width="stretch")

top_provinces = (
    filtered_df.groupby("province", as_index=False)["affected_persons"]
    .sum()
    .sort_values("affected_persons", ascending=False)
    .head(10)
)

fig_provinces = px.bar(
    top_provinces,
    x="province",
    y="affected_persons",
    title="Top Affected Provinces by Affected Persons",
    labels={"province": "Province", "affected_persons": "Affected persons"},
)
right_chart.plotly_chart(fig_provinces, width="stretch")

events_over_time = (
    filtered_df.assign(event_day=filtered_df["event_date"].dt.date)
    .groupby("event_day", as_index=False)
    .size()
    .rename(columns={"event_day": "date", "size": "flood_events"})
)

fig_time = px.line(
    events_over_time,
    x="date",
    y="flood_events",
    markers=True,
    title="Flood Events Over Time",
    labels={"date": "Date", "flood_events": "Flood events"},
)
st.plotly_chart(fig_time, width="stretch")

map_df = filtered_df[(filtered_df["latitude"] != 0) & (filtered_df["longitude"] != 0)].copy()

fig_map = px.scatter_map(
    map_df,
    lat="latitude",
    lon="longitude",
    size="affected_persons",
    color="region",
    hover_name="municipality",
    hover_data=["province", "event_date", "affected_families", "affected_persons"],
    zoom=4.5,
    height=520,
    title="Flood Event Locations",
)
fig_map.update_layout(map_style="open-street-map", margin={"r": 0, "t": 45, "l": 0, "b": 0})
st.plotly_chart(fig_map, width="stretch")

st.subheader("Flood Event Records")
st.dataframe(
    filtered_df[
        [
            "event_date",
            "region",
            "province",
            "municipality",
            "flood_area",
            "affected_families",
            "affected_persons",
            "source",
        ]
    ],
    width="stretch",
    hide_index=True,
)
