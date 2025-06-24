from . import db
from sqlalchemy import func

class VevorWeatherData(db.Model):
    __tablename__ = 'vevor_weather_data'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    timestamp_utc = db.Column(db.DateTime)
    temperature_f = db.Column(db.Float)
    temperature_c = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    pressure_in = db.Column(db.Float)
    dewpoint_f = db.Column(db.Float)
    dewpoint_c = db.Column(db.Float)
    windspeed_mph = db.Column(db.Float)
    windspeed_kmph = db.Column(db.Float)
    winddir_deg = db.Column(db.Integer)
    rainfall_in = db.Column(db.Float)
    uv = db.Column(db.Integer)
    solarradiation = db.Column(db.Float)
    received_at = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f'<VevorWeatherData id={self.id} station_id={self.station_id} timestamp_utc={self.timestamp_utc}>' 