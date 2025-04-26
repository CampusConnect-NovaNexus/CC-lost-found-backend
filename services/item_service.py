from flask import g, jsonify
from .. import db
from ..models.item_model import Item
from ..services.image_upload_service import image_upload

def get_all_items():
    try:
        items = db.session.query(Item).all()
        return jsonify([item.json() for item in items]), 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def get_item(item_id):
    try:
        item = db.session.query(Item).filter_by(_id=item_id).first()
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item.json()), 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def get_multiple_items(item_ids):
    try:
        items = db.session.query(Item).filter(Item._id.in_(item_ids)).all()
        if not items:
            return jsonify({"error": "Items not found"}), 404
        return jsonify([item.json() for item in items]), 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def create_item(data):
    title = data.get('title')
    description = data.get('description')
    image_file = data.get('image_file')  # This should be the file object from request.files
    user_id = data.get('user_id')
    if not user_id:
        return {"error": "User ID is required"}, 400
    item_category = data.get('item_category')
    
    image_url = None
    # Handle image upload if image file is provided
    if image_file:
        filename = f"{user_id}_{title}_{image_file.filename}"
        upload_response = image_upload(image_file, filename)
        if upload_response:
            # Extract the URL from the ImageKit response
            image_url = upload_response.get('url')
    
    try:
        new_item = Item(
            item_title=title, 
            item_description=description, 
            user_id=user_id, 
            item_image=image_url,  # Store the image URL from upload
            item_category=item_category
        )
        db.session.add(new_item)
        db.session.commit()
        return {"status": "Item created successfully", "item_id": new_item._id, "image_url": image_url}, 201
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def update_item(data):
    _id = data.get('_id')
    title = data.get('title')
    description = data.get('description')
    image = data.get('image')
    user_id = data.get('user_id')

    try:
        item = db.session.query(Item).filter_by(_id=_id).first()
        if not item:
            return {"error": "Item not found"}, 404

        if title:
            item.item_title = title
        if description:
            item.item_description = description
        if image:
            item.item_image = image
        if user_id:
            item.user_id = user_id

        db.session.commit()
        return {"status": "Item updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500

def delete_item(data):
    _id = data.get('_id')

    try:
        item = db.session.query(Item).filter_by(_id=_id).first()
        if not item:
            return {"error": "Item not found"}, 404

        db.session.delete(item)
        db.session.commit()
        return {"status": "Item deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
        return jsonify({"error": f"Database error: {str(error)}"}), 500