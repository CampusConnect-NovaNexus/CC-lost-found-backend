from flask import Blueprint, request
from services.user_service import *
user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_user_list_view():
    return get_all_users()

@user_bp.route('/<string:user_id>', methods=['GET'])
def get_user_view(user_id):
    if not user_id:
        return {'error': 'No user ID provided'}, 400
    return get_user(user_id)

@user_bp.route('/register', methods=['POST'])
def create_user_view():
    data = request.get_json()
    return create_user(data)


@user_bp.route('/update', methods=['POST'])
def update_user_view():
    data = request.get_json()
    return update_user(data)

@user_bp.route('/delete', methods=['POST'])
def delete_user_view():
    data = request.get_json()
    return delete_user(data)
