from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS

migrate = Migrate()

jwt = JWTManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app)

    jwt.init_app(app)
    db.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from models.user_model import Users
    from models.item_model import Item
    from models.device_model import Devices
    
    # Import and register blueprints
    from routes.item_routes import item_bp
    from routes.user_routes import user_bp
    from routes.auth_routes import auth_bp
    from routes.ai_routes import ai_routes_bp
    from routes.notification_routes import notification_bp

    migrate.init_app(app, db)

    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(item_bp, url_prefix='/api/v1/item')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(ai_routes_bp, url_prefix='/api/v1/ai')
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notification')

    # Create tables on app startup if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created (if they didn't exist already)")

    # create route for health check
    @app.route('/', methods=['GET'])
    def health_check():
        return {"status": "healthy"}, 200
    
    return app
