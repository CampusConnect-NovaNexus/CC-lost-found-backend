from flask import Blueprint, request
from backend.services.auth_service import login
from backend.schemas.auth_schemas import login_schema
from marshmallow.exceptions import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_view():
    try:
        login_schema.load(request.json)
    except ValidationError as err:
        return {'error': 'Invalid input', 'details': err.messages}, 400
    
    return login(request.json)