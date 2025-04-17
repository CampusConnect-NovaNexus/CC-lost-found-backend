from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask import jsonify
from datetime import timedelta

def login(data): 
    username = data.get('username')
    password = data.get('password')

    # database lookup

    user = {
        'id': 1,
        'username': username,
        'password': password
    }

    access_token = create_access_token(identity=user['id'])
    refresh_token = create_refresh_token(identity=user['id'])

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    