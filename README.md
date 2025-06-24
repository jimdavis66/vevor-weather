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
   pip install -r requirements.txt
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
- `ALLOWED_IPS`: (Optional) Comma-separated list of allowed IPs
- `LOG_LEVEL` : (Optional) DEBUG, INFO, WARNING, ERROR, or CRITICAL

## Docker
To build and run with Docker:
```bash
docker build -t vevor-weather .
docker run --env-file .env vevor-weather
```

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
    temperature_c REAL,
    humidity INTEGER,
    pressure_in REAL,
    dewpoint_f REAL,
    dewpoint_c REAL,
    windspeed_mph REAL,
    windspeed_kmph REAL,
    winddir_deg INTEGER,
    rainfall_in REAL,
    uv INTEGER,
    solarRadiation REAL,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
