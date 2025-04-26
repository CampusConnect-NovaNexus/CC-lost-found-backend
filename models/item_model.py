import uuid
from .. import db

class Item(db.Model):
    __tablename__ = 'items'
    _id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_title = db.Column(db.String(80), nullable=False)
    item_description = db.Column(db.String(200), nullable=False)
    item_image = db.Column(db.String(200), nullable=True)
    item_category = db.Column(db.Enum('LOST', 'FOUND', name='item_category'), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)

    def __init__(self, item_title, item_description, user_id, item_image=None, item_category='FOUND'):
        self.item_title = item_title
        self.item_description = item_description
        self.item_image = item_image
        self.user_id = user_id
        self.item_category = item_category

    def json(self):
        return {
            "id": self._id,
            "item_title": self.item_title,
            "item_description": self.item_description,
            "item_image": self.item_image,
            "item_category": self.item_category,
            "user_id": self.user_id
        }


