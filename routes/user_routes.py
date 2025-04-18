from flask import Blueprint, request
from backend.services.user_service import get_user, get_all_users

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_user_list_view():
    return get_all_users()

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_view(user_id):
    if not user_id:
        return {'error': 'No user ID provided'}, 400
    return get_user(user_id)