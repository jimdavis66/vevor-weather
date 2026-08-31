import logging
from datetime import datetime, timezone

import requests
from flask import Blueprint, Response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .models import VevorWeatherData

bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@bp.route("/weatherstation/updateweatherstation.php", methods=["GET"])
def update_weatherstation():
    params = request.args.to_dict()
    redacted_params = {
        key: ("[REDACTED]" if key.upper() == "PASSWORD" else value)
        for key, value in params.items()
    }
    logger.info("Received params: %s", redacted_params)

    # Required fields
    required_fields = ["ID", "dateutc"]
    for field in required_fields:
        if field not in params:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Parse and convert fields
    try:
        data = VevorWeatherData(
            station_id=params.get("ID"),
            timestamp_utc=parse_date(params.get("dateutc")),
            temperature_f=safe_float(params.get("tempf")),
            humidity=safe_int(params.get("humidity")),
            pressure_in=safe_float(params.get("baromin")),
            dewpoint_f=safe_float(params.get("dewptf")),
            windspeed_mph=safe_float(params.get("windspeedmph")),
            windgust_mph=safe_float(params.get("windgustmph")),
            winddir_deg=safe_int(params.get("winddir")),
            rainfall_in=safe_float(params.get("rainin")),
            uv=safe_int(params.get("UV")),
            solar_radiation=safe_float(params.get("solarRadiation")),
        )
        db.session.add(data)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        logger.error("Database write failed")

    # Forward the request
    try:
        forward_url = (
            "http://rtupdate.wunderground.com/weatherstation/"
            "updateweatherstation.php"
        )
        resp = requests.get(forward_url, params=request.args, timeout=5)
        logger.info("Forwarded to WU, status: %s", resp.status_code)
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get("Content-Type", "text/plain"),
        )
    except requests.RequestException:
        logger.error("Weather Underground forwarding failed")
        return jsonify({"error": "Failed to forward to Weather Underground"}), 502


def safe_float(val):
    try:
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def safe_int(val):
    try:
        return int(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def parse_date(date_str):
    try:
        # Handles 'now' or UTC string
        if date_str == "now":
            return datetime.now(timezone.utc)
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )
    except (TypeError, ValueError):
        return None
