from flask import Blueprint, request
from ..services.image_upload_service import *

image_upload_bp = Blueprint('image_upload', __name__)

@image_upload_bp.route('/', methods=['POST'])
def image_upload_view():
    file = request.files.get('file')
    filename = request.form.get('filename')
    return image_upload(file, filename)