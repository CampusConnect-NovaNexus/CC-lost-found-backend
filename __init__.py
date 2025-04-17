from flask import Flask
from backend.routes.user_routes import user_bp
from backend.routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    jwt.init_app(app)

    load_dotenv()  # Load environment variables from a .env file
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # 15 minutes
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30) # 30 days

    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    
    return app


