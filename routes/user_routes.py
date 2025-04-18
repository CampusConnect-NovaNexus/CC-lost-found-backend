from flask import Blueprint, request

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_user_list_view():
    from backend.services.user_service import get_all_users  
    return get_all_users()

@user_bp.route('/<string:user_id>', methods=['GET'])
def get_user_view(user_id):
    if not user_id:
        return {'error': 'No user ID provided'}, 400
    from backend.services.user_service import get_user  
    return get_user(user_id)

@user_bp.route('/register', methods=['POST'])
def create_user_view():
    data = request.get_json()
    from backend.services.user_service import create_user  
    return create_user(data)


@user_bp.route('/update', methods=['POST'])
def update_user_view():
    data = request.get_json()
    from backend.services.user_service import update_user
    return update_user(data)

@user_bp.route('/delete', methods=['POST'])
def delete_user_view():
    data = request.get_json()
    from backend.services.user_service import delete_user
    return delete_user(data)
