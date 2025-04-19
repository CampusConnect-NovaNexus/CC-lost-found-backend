from flask import jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user_model import Users
import traceback

def login_user(data):
    try:
        # Debug log
        current_app.logger.info(f"Login attempt for email: {data.get('email', 'Not provided')}")
        
        # Extract login data
        email = data.get('email', None)
        password = data.get('password', None)
        
        # Check for missing fields
        if not email or not password:
            current_app.logger.warning("Login missing email or password")
            return {'error': 'Missing email or password'}, 400
        
        # Look up user by email
        user = Users.query.filter_by(email=email).first()
        
        # Check if user exists and password matches
        if not user:
            current_app.logger.warning(f"Login failed: User with email {email} not found")
            return {'error': 'Invalid email or password'}, 401
            
        if not check_password_hash(user.password, password):
            current_app.logger.warning(f"Login failed: Invalid password for user {email}")
            return {'error': 'Invalid email or password'}, 401
        
        # Create tokens
        access_token = create_access_token(identity=user._id)
        refresh_token = create_refresh_token(identity=user._id)
        
        current_app.logger.info(f"Login successful for user: {user.username}")
        
        # Return tokens and user data
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.json()
        }, 200
        
    except Exception as e:
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Login error: {str(e)}\n{error_trace}")
        return {'error': str(e)}, 500