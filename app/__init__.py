import sentry_sdk
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

sentry_sdk.init(
    dsn="https://2e740bef9a83022b54bf177f37ba0e23@o339642.ingest.us.sentry.io/4508683419975680",
    traces_sample_rate=1.0,
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