# **Product Requirements Document (PRD)**

**Title:** Weather Station Proxy Web App
**Author:** James Davis
**Date:** 2025-06-24
**Version:** 1.0

---

## **1. Overview**

This project is a lightweight Python web application that acts as a proxy between a Vevor weather station and Weather Underground. The app will accept incoming **GET** requests containing weather data, extract and store relevant metrics into a **PostgreSQL** database, and then forward the **original** request to **Weather Underground** as-is.

---

## **2. Goals and Objectives**

* **Capture** weather telemetry data sent via GET from a Vevor weather station.
* **Parse and store** key weather metrics in a PostgreSQL database.
* **Forward** the exact original request to Weather Underground to preserve existing integrations.
* Be **lightweight**, **secure**, and **maintainable**.

---

## **3. Functional Requirements**

### 3.1 API Endpoint

* **Method**: `GET`
* **Path**: `/weatherstation/updateweatherstation.php`
* **Authentication**: Optional or IP-based allowlist

### 3.2 Expected Query Parameters

The app should accept and parse the following example parameters (subject to what Vevor sends):

* `ID`: Weather Underground station ID
* `dateutc`: Timestamp of the reading
* `tempf`, `humidity`, `baromin`, `dewptf`, `dewptc`, `windspeedmph`, `winddir`, `windgustmph`, `rainin`, `dailyrainin`, `UV`, and `solarRadiation`.

The app must log all parameters received for full traceability.

### 3.3 Data Handling

* Parse relevant values from the GET request
* Store a new row in PostgreSQL with:

  * Timestamp
  * Temperature (°F)
  * Temperature (°C)
  * Humidity (%)
  * Pressure (inHg)
  * Dew Point (°F)
  * Dew Point (°C)
  * Wind Speed (mph)
  * Wind Speed (kmph)
  * Wind Direction (°)
  * Rainfall (in)
  * Station ID

### 3.4 Forwarding Logic

* Reconstruct and forward the **exact** GET request to:

  ```
  https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?[original_query]
  ```
* Capture and log the HTTP response code from Weather Underground.
* Return the same HTTP response back to the weather station.

---

## **4. Non-Functional Requirements**

* **Tech Stack**: Python 3.13+, Flask, PostgreSQL, SQLAlchemy
* **Deployment**: Docker container
* **Monitoring**: Basic logging to stdout
* **Security**:
  * All secrets and configuration options are passed as environment variables
  * Allow IP whitelisting for incoming connections
* **Performance**:
  * Must handle 1 request/second sustained load
  * Max end-to-end latency: < 500ms

---

## **5. Database Schema Proposal (PostgreSQL)**

```sql
CREATE TABLE vevor_weather_data (
    id SERIAL PRIMARY KEY,
    station_id TEXT,
    timestamp_utc TIMESTAMP,
    temperature_f REAL,
    temperature_d REAL,
    humidity INTEGER,
    pressure_in REAL,
    dewpoint_f REAL,
    dewpoint_c REAL,
    windspeed_mph REAL,
    windspeed_kmph REAL,
    winddir_deg INTEGER,
    rainfall_in REAL,
    uv INTEGER,
    solarRadiation REAL
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## **6. Error Handling**

* If the incoming GET request is missing mandatory fields, return `400 Bad Request`.
* If DB write fails, log the error and continue to forward the request.
* If forwarding to Weather Underground fails, return `502 Bad Gateway` but still save the data locally.

---

## **9. Milestones**

| Milestone                    | Target Date |
| ---------------------------- | ----------- |
| Initial API + DB integration | Week 1      |
| Forwarding logic complete    | Week 2      |
| Dockerization + Deployment   | Week 3      |
| Testing & Documentation      | Week 4      |

---

