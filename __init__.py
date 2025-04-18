from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.routes.item_routes import item_bp
from backend.routes.user_routes import user_bp
from flask_jwt_extended import JWTManager
from backend.config import Config
from flask_migrate import Migrate

migrate = Migrate()

jwt = JWTManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(item_bp, url_prefix='/api/v1/item')

    # Create tables on app startup if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created (if they didn't exist already)")
    
    return app
