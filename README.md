# Weather Station Proxy Web App

## Overview
This is a lightweight Python web application that acts as a proxy between a Vevor weather station and Weather Underground. It captures weather telemetry data, stores key metrics in a PostgreSQL database, and forwards the original request to Weather Underground.

## Features
- Accepts GET requests from Vevor weather stations
- Parses and stores weather data in PostgreSQL
- Forwards requests to Weather Underground
- Lightweight, secure, and maintainable

## Setup
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements/requirements.txt
   ```
4. Set environment variables (see below)
5. Run the app:
   ```bash
   python -m app
   ```

## Environment Variables
- `PORT`: App listening port 
- `DATABASE_URL`: PostgreSQL connection string eg. `postgresql+psycopg2://user:pass@host:5432/vevor_weather`
- `SECRET_KEY`: Flask secret key
- `LOG_LEVEL` : (Optional) DEBUG, INFO, WARNING, ERROR, or CRITICAL

## Docker
To build and run with Docker:
```bash
docker build -t vevor-weather .
docker run --env-file .env vevor-weather
```

### Why `app/gunicorn_entrypoint.py` exists
This image is built on a minimal Python base that **does not include a shell** (no `sh`). That means we can’t reliably use a shell-form `CMD` like `sh -c "gunicorn ..."` to expand environment variables.

Instead, `app/gunicorn_entrypoint.py` reads runtime settings from environment variables (like `PORT`, worker/thread counts, timeouts) and then `exec()`s `gunicorn` directly, which is more robust in minimal containers and keeps configuration env-driven.

## API
- **GET** `/weatherstation/updateweatherstation.php` — Accepts weather data as query parameters

## Database Setup

Before running the app, ensure your PostgreSQL database has a table named `vevor_weather_data` ready to write to. You can create it with the following SQL:

```sql
CREATE TABLE vevor_weather_data (
    id SERIAL PRIMARY KEY,
    station_id TEXT,
    timestamp_utc TIMESTAMP,
    temperature_f REAL,
    humidity INTEGER,
    pressure_in REAL,
    dewpoint_f REAL,
    windspeed_mph REAL,
    windgust_mph REAL,
    winddir_deg INTEGER,
    rainfall_in REAL,
    uv INTEGER,
    solar_radiation REAL,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
GRANT ALL ON vevor_weather_data TO vevor;
GRANT ALL ON SCHEMA public TO vevor;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO vevor;
```
