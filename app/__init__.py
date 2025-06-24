import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from dotenv import load_dotenv
import logging

load_dotenv()

db = SQLAlchemy()

def test_db_connection_and_table(app):
    with app.app_context():
        try:
            # Test connection
            db.session.execute(text('SELECT 1'))
            # Check table exists
            inspector = inspect(db.engine)
            if 'vevor_weather_data' not in inspector.get_table_names():
                raise Exception('Table vevor_weather_data does not exist!')
            print('Database connection and table check: OK')
        except Exception as e:
            print(f'Database check failed: {e}')
            raise

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

    db.init_app(app)

    # Set logging level
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

    test_db_connection_and_table(app)

    from . import routes
    app.register_blueprint(routes.bp)

    return app 