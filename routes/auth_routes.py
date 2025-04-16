from flask import Blueprint, request
from backend.services.auth_service import login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_view():
    data = request.get_json()
    if not data:
        return {'error': 'No data provided'}, 400
    if 'username' not in data or 'password' not in data:
        return {'error': 'Username and password required'}, 400
    return login(data)