from flask import Blueprint, request
from ..services.item_service import *

item_bp = Blueprint('item', __name__)

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