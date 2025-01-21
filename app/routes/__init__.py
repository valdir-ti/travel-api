def register_routes(app):
    from app.routes.destinations import destinations_bp
    app.register_blueprint(destinations_bp)