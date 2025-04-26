from flask import g, Blueprint, request
from ..services.item_service import *
from ..grpc.grpc_fns import validate_token
import jwt

item_bp = Blueprint('item', __name__)

@item_bp.before_request
def before_request():
    authorization = request.headers.get('authorization')
    if not authorization:
        return {"error": "Unauthorized"}, 401
    token = authorization.split(" ")[1]
    if not token:
        return {"error": "Unauthorized"}, 401
    if (validate_token(token) == False):
        return {"error": "Unauthorized"}, 401
    payload = jwt.decode(token, options={"verify_signature": False})
    if not payload:
        return {"error": "Unauthorized"}, 401
    g.user_id = payload.get('userId')
    g.email_id = payload.get('userEmail')

@item_bp.route('/', methods=['GET'])
def get_item_list_view():
    return get_all_items()
    
@item_bp.route('/getItems', methods=['POST'])
def get_multiple_items_view():
    data = request.get_json()
    item_ids = data.get('item_ids', [])
    if not item_ids:
        return {'error': 'No item IDs provided'}, 400
    return get_multiple_items(item_ids)

@item_bp.route('/create', methods=['POST'])
def create_item_view():
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'user_id': request.form.get('user_id'),
            'item_category': request.form.get('item_category'),
            'image_file': request.files.get('image_file') if 'image_file' in request.files else None
        }

        print("Data from form:", data)
    else:
        data = request.get_json()
        
    return create_item(data)

@item_bp.route('/update', methods=['POST'])
def update_item_view():
    data = request.get_json()
    return update_item(data)

@item_bp.route('/delete', methods=['POST'])
def delete_item_view():
    data = request.get_json()
    return delete_item(data)

@item_bp.route('/<string:item_id>', methods=['GET'])
def get_item_view(item_id):
    if not item_id:
        return {'error': 'No item ID provided'}, 400
    return get_item(item_id)