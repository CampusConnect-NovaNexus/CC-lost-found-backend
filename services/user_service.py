# from flask import jsonify, current_app
# from werkzeug.security import generate_password_hash
# from flask_jwt_extended import create_access_token, create_refresh_token
# from ..models.user_model import Users
# from .. import db
# import traceback

# def get_user(user_id):
#     try:
#         user = Users.query.filter_by(_id=user_id).first()
#         if user:
#             return user.json()
#         return {"error": "User not found"}, 404
#     except Exception as e:
#         current_app.logger.error(f"Error getting user: {str(e)}")
#         return {"error": str(e)}, 500

# def get_all_users():
#     try:
#         users = Users.query.all()
#         return jsonify([user.json() for user in users])
#     except Exception as e:
#         current_app.logger.error(f"Error getting all users: {str(e)}")
#         return {"error": str(e)}, 500

# def create_user(data):
#     # Debug log
#     current_app.logger.info(f"Received registration data: {data}")
    
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     # Validate required fields
#     if not username or not email or not password:
#         current_app.logger.warning("Registration missing required fields")
#         return {"error": "Missing required fields"}, 400

#     try:
#         # Check if user already exists
#         existing_user = Users.query.filter_by(email=email).first()
#         if existing_user:
#             current_app.logger.warning(f"Email already registered: {email}")
#             return {"error": "Email already registered"}, 409

#         # Hash the password
#         hashed_password = generate_password_hash(password)
#         current_app.logger.debug("Password hashed successfully")
        
#         # Create new user
#         new_user = Users(username=username, email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         current_app.logger.info(f"User created successfully: {username}, ID: {new_user._id}")
        
#         # Generate tokens
#         access_token = create_access_token(identity=new_user._id)
#         refresh_token = create_refresh_token(identity=new_user._id)
        
#         # Return user data and tokens
#         return {
#             "message": "User registered successfully",
#             "user": new_user.json(),
#             "access_token": access_token,
#             "refresh_token": refresh_token
#         }, 201
#     except Exception as e:
#         db.session.rollback()
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Registration error: {str(e)}\n{error_trace}")
        
#         error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
#         return {"error": f"Database error: {str(error)}"}, 500

# def update_user(data):
#     # Debug log
#     current_app.logger.info(f"Received update user data: {data}")
    
#     _id = data.get('_id')
#     username = data.get('username')
#     email = data.get('email')
#     current_password = data.get('currentPassword')
#     new_password = data.get('newPassword')

#     try:
#         user = Users.query.filter_by(_id=_id).first()
#         if not user:
#             current_app.logger.warning(f"User not found for update: {_id}")
#             return {"error": "User not found"}, 404

#         if username:
#             user.username = username
#         if email:
#             user.email = email
#         if current_password and new_password:
#             # This would need password verification logic
#             user.password = generate_password_hash(new_password)

#         db.session.commit()
#         current_app.logger.info(f"User updated successfully: {_id}")
#         return {"message": "User updated successfully", "user": user.json()}, 200
#     except Exception as e:
#         db.session.rollback()
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"User update error: {str(e)}\n{error_trace}")
        
#         error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
#         return {"error": f"Database error: {str(error)}"}, 500

# def delete_user(data):
#     # Debug log
#     current_app.logger.info(f"Received delete user data: {data}")
    
#     _id = data.get('_id')

#     try:
#         user = Users.query.filter_by(_id=_id).first()
#         if not user:
#             current_app.logger.warning(f"User not found for deletion: {_id}")
#             return {"error": "User not found"}, 404

#         db.session.delete(user)
#         db.session.commit()
#         current_app.logger.info(f"User deleted successfully: {_id}")
#         return {"message": "User deleted successfully"}, 200
#     except Exception as e:
#         db.session.rollback()
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"User deletion error: {str(e)}\n{error_trace}")
        
#         error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
#         return {"error": f"Database error: {str(error)}"}, 500