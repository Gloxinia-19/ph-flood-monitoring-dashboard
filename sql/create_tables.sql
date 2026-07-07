CREATE TABLE IF NOT EXISTS flood_events (
    event_id SERIAL PRIMARY KEY,
    event_date DATE,
    region TEXT,
    province TEXT,
    municipality TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    flood_area NUMERIC,
    affected_families INTEGER,
    affected_persons INTEGER,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
