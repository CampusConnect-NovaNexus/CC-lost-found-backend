from flask import Blueprint, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_view():
    data = request.get_json()
    from backend.services.auth_service import login_user
    return login_user(data)