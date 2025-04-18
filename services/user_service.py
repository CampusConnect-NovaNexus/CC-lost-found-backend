from flask import jsonify
from backend.models.user_model import Users
from backend import db

def get_user(user_id):
    return { user_id: "User data" } 

def get_all_users():
    pass

def create_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"status": "User created successfully", "user_id": new_user._id}, 201
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def update_user(data):
    user_id = data.get('user_id')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        user = Users.query.filter_by(_id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password

        db.session.commit()
        return {"status": "User updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def delete_user(data):
    user_id = data.get('user_id')

    try:
        user = Users.query.filter_by(_id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"status": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500