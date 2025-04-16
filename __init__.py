from flask import Flask
from backend.routes.user_routes import user_bp
from backend.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    return app


