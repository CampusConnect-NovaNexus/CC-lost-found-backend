from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.notification_service import (
    register_device, 
    update_device_token, 
    remove_device, 
    send_notification_to_user,
    send_notification_to_all
)

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/register', methods=['POST'])
@jwt_required()
def register_device_route():
    """
    Register a device for push notifications
    Required fields:
    - expo_token: string
    - platform: string ('ios' or 'android')
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'expo_token' not in data or 'platform' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    return register_device(user_id, data['expo_token'], data['platform'])

@notification_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_device_token_route():
    """
    Update an existing device token
    Required fields:
    - old_token: string
    - new_token: string
    - platform: string ('ios' or 'android')
    """
    data = request.get_json()
    
    if not data or 'old_token' not in data or 'new_token' not in data or 'platform' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    return update_device_token(data['old_token'], data['new_token'], data['platform'])

@notification_bp.route('/remove', methods=['DELETE'])
@jwt_required()
def remove_device_route():
    """
    Remove a device from the database
    Required fields:
    - expo_token: string
    """
    data = request.get_json()
    
    if not data or 'expo_token' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    return remove_device(data['expo_token'])

@notification_bp.route('/send', methods=['POST'])
@jwt_required()
def send_notification_route():
    """
    Send a notification to a specific user
    Required fields:
    - user_id: string (optional, if not provided, sends to current user)
    - title: string
    - body: string
    - data: object (optional)
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'title' not in data or 'body' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    # If user_id is not provided, send to current user
    user_id = data.get('user_id', current_user_id)
    
    # Check if the current user is trying to send to another user
    if user_id != current_user_id:
        # Here you could add authorization checks
        pass
        
    return send_notification_to_user(
        user_id, 
        data['title'], 
        data['body'], 
        data.get('data')
    )

@notification_bp.route('/send-all', methods=['POST'])
@jwt_required()
def send_notification_to_all_route():
    """
    Send a notification to all registered devices
    Required fields:
    - title: string
    - body: string
    - data: object (optional)
    """
    # This endpoint should be restricted to admins
    # You should add authorization checks here
    
    data = request.get_json()
    
    if not data or 'title' not in data or 'body' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    return send_notification_to_all(
        data['title'], 
        data['body'], 
        data.get('data')
    )