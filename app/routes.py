import logging
from flask import Blueprint, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
import requests
from datetime import datetime, timezone
from . import db
from .models import VevorWeatherData

bp = Blueprint('main', __name__)


@bp.route('/weatherstation/updateweatherstation.php', methods=['GET'])
def update_weatherstation():
    params = request.args.to_dict()
    redacted_params = {
        key: ('[REDACTED]' if key.upper() == 'PASSWORD' else value)
        for key, value in params.items()
    }
    logging.info(f"Received params: {redacted_params}")

    # Required fields
    required_fields = ['ID', 'dateutc']
    for field in required_fields:
        if field not in params:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Parse and convert fields
    try:
        data = VevorWeatherData(
            station_id=params.get('ID'),
            timestamp_utc=parse_date(params.get('dateutc')),
            temperature_f=safe_float(params.get('tempf')),
            humidity=safe_int(params.get('humidity')),
            pressure_in=safe_float(params.get('baromin')),
            dewpoint_f=safe_float(params.get('dewptf')),
            windspeed_mph=safe_float(params.get('windspeedmph')),
            windgust_mph=safe_float(params.get('windgustmph')),
            winddir_deg=safe_int(params.get('winddir')),
            rainfall_in=safe_float(params.get('rainin')),
            uv=safe_int(params.get('UV')),
            solar_radiation=safe_float(params.get('solarRadiation')),
        )
        db.session.add(data)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"DB error: {e}")
    except Exception as e:
        logging.error(f"Parse error: {e}")

    # Forward the request
    try:
        forward_url = f"http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?{request.query_string.decode()}"
        resp = requests.get(forward_url, timeout=5)
        logging.info(f"Forwarded to WU, status: {resp.status_code}")
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type', 'text/plain'))
    except Exception as e:
        logging.error(f"Forwarding error: {e}")
        return jsonify({'error': 'Failed to forward to Weather Underground'}), 502

def safe_float(val):
    try:
        return float(val) if val is not None else None
    except Exception:
        return None

def safe_int(val):
    try:
        return int(val) if val is not None else None
    except Exception:
        return None

def parse_date(date_str):
    try:
        # Handles 'now' or UTC string
        if date_str == 'now':
            return datetime.now(timezone.utc)
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(
            tzinfo=timezone.utc
        )
    except Exception:
        return None 