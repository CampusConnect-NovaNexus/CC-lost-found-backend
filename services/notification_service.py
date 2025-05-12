# from flask import current_app
# import requests
# import json
# from models.device_model import Devices
# from __init__ import db
# import traceback
# import time

# # Constants
# EXPO_PUSH_API = "https://exp.host/--/api/v2/push/send"
# MAX_RETRIES = 3
# BACKOFF_FACTOR = 2  # seconds

# def register_device(user_id, expo_token, platform):
#     """
#     Register a device for push notifications
#     """
#     try:
#         # Check if the device token already exists
#         existing_device = Devices.query.filter_by(expo_token=expo_token).first()
        
#         if existing_device:
#             # If the device exists but belongs to a different user, update the user_id
#             if existing_device.user_id != user_id:
#                 existing_device.user_id = user_id
#                 existing_device.platform = platform
#                 db.session.commit()
#                 current_app.logger.info(f"Updated device token {expo_token} to user {user_id}")
#             return {"message": "Device token updated", "device_id": existing_device._id}, 200
        
#         # Create a new device
#         new_device = Devices(user_id=user_id, expo_token=expo_token, platform=platform)
#         db.session.add(new_device)
#         db.session.commit()
        
#         current_app.logger.info(f"Registered new device token for user {user_id}")
#         return {"message": "Device registered successfully", "device_id": new_device._id}, 201
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Error registering device: {str(e)}\n{error_trace}")
#         db.session.rollback()
#         return {"error": str(e)}, 500

# def update_device_token(old_token, new_token, platform):
#     """
#     Update an existing device token
#     """
#     try:
#         device = Devices.query.filter_by(expo_token=old_token).first()
        
#         if not device:
#             current_app.logger.warning(f"Device with token {old_token} not found")
#             return {"error": "Device not found"}, 404
            
#         device.expo_token = new_token
#         device.platform = platform
#         db.session.commit()
        
#         current_app.logger.info(f"Updated device token from {old_token} to {new_token}")
#         return {"message": "Device token updated successfully"}, 200
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Error updating device token: {str(e)}\n{error_trace}")
#         db.session.rollback()
#         return {"error": str(e)}, 500

# def remove_device(expo_token):
#     """
#     Remove a device from the database
#     """
#     try:
#         device = Devices.query.filter_by(expo_token=expo_token).first()
        
#         if not device:
#             current_app.logger.warning(f"Device with token {expo_token} not found for removal")
#             return {"error": "Device not found"}, 404
            
#         db.session.delete(device)
#         db.session.commit()
        
#         current_app.logger.info(f"Removed device token {expo_token}")
#         return {"message": "Device removed successfully"}, 200
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Error removing device: {str(e)}\n{error_trace}")
#         db.session.rollback()
#         return {"error": str(e)}, 500

# def send_notification_to_user(user_id, title, body, data=None):
#     """
#     Send a notification to all devices of a specific user
#     """
#     try:
#         devices = Devices.query.filter_by(user_id=user_id).all()
        
#         if not devices:
#             current_app.logger.warning(f"No devices found for user {user_id}")
#             return {"message": "No devices registered for this user"}, 404
            
#         results = []
#         for device in devices:
#             result = _send_push_notification(
#                 device.expo_token, 
#                 title, 
#                 body, 
#                 data
#             )
#             results.append({"device_id": device._id, "result": result})
            
#         return {"message": "Notifications sent", "results": results}, 200
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Error sending notification to user: {str(e)}\n{error_trace}")
#         return {"error": str(e)}, 500

# def send_notification_to_all(title, body, data=None):
#     """
#     Send a notification to all registered devices
#     """
#     try:
#         devices = Devices.query.all()
        
#         if not devices:
#             current_app.logger.warning("No devices found in the database")
#             return {"message": "No devices registered"}, 404
            
#         results = []
#         for device in devices:
#             result = _send_push_notification(
#                 device.expo_token, 
#                 title, 
#                 body, 
#                 data
#             )
#             results.append({"device_id": device._id, "result": result})
            
#         return {"message": "Notifications sent to all devices", "results": results}, 200
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Error sending notification to all: {str(e)}\n{error_trace}")
#         return {"error": str(e)}, 500

# def _send_push_notification(expo_token, title, body, data=None, retry_count=0):
#     """
#     Send a push notification to a specific Expo push token with retry logic
#     """
#     try:
#         message = {
#             "to": expo_token,
#             "sound": "default",
#             "title": title,
#             "body": body,
#             "data": data or {}
#         }
        
#         headers = {
#             "Accept": "application/json",
#             "Accept-Encoding": "gzip, deflate",
#             "Content-Type": "application/json",
#         }
        
#         response = requests.post(
#             EXPO_PUSH_API,
#             headers=headers,
#             data=json.dumps(message)
#         )
        
#         response_data = response.json()
        
#         # Check for errors that indicate the token is invalid
#         if response.status_code != 200:
#             current_app.logger.error(f"Error sending push notification: {response_data}")
            
#             # If we haven't exceeded max retries, try again with exponential backoff
#             if retry_count < MAX_RETRIES:
#                 wait_time = BACKOFF_FACTOR * (2 ** retry_count)
#                 current_app.logger.info(f"Retrying in {wait_time} seconds...")
#                 time.sleep(wait_time)
#                 return _send_push_notification(expo_token, title, body, data, retry_count + 1)
                
#             return {"success": False, "error": response_data}
            
#         # Check for specific error types in the response
#         if "data" in response_data and response_data["data"]:
#             for item in response_data["data"]:
#                 if "status" in item and item["status"] == "error":
#                     # Handle DeviceNotRegistered error by removing the token
#                     if "details" in item and item["details"].get("error") == "DeviceNotRegistered":
#                         current_app.logger.warning(f"Device not registered: {expo_token}")
#                         remove_device(expo_token)
#                     return {"success": False, "error": item["message"]}
                    
#         return {"success": True, "data": response_data}
        
#     except Exception as e:
#         error_trace = traceback.format_exc()
#         current_app.logger.error(f"Exception sending push notification: {str(e)}\n{error_trace}")
        
#         # If we haven't exceeded max retries, try again with exponential backoff
#         if retry_count < MAX_RETRIES:
#             wait_time = BACKOFF_FACTOR * (2 ** retry_count)
#             current_app.logger.info(f"Retrying in {wait_time} seconds...")
#             time.sleep(wait_time)
#             return _send_push_notification(expo_token, title, body, data, retry_count + 1)
            
#         return {"success": False, "error": str(e)}