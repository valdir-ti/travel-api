import os
import sentry_sdk
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

enviroment=os.getenv('ENVIROMENT'),
sentry_dns=os.getenv('SENTRY_DSN')

sentry_sdk.init(
    dsn=sentry_dns,
    traces_sample_rate=1.0,
    environment=enviroment,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        from app.models import Destination
        db.create_all()
        
    from app.routes import register_routes
    register_routes(app)
    
    return app