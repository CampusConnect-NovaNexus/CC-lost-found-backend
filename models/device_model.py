from __init__ import db
import uuid
from datetime import datetime

class Devices(db.Model):
    __tablename__ = 'devices'
    _id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users._id'), nullable=False)
    expo_token = db.Column(db.String(150), unique=True, nullable=False)
    platform = db.Column(db.String(20), nullable=False)  # 'ios' or 'android'
    last_used = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc))
    
    def __init__(self, user_id, expo_token, platform):
        self.user_id = user_id
        self.expo_token = expo_token
        self.platform = platform
    
    def json(self):
        return {
            "id": self._id,
            "user_id": self.user_id,
            "expo_token": self.expo_token,
            "platform": self.platform,
            "last_used": self.last_used.isoformat() if self.last_used else None
        }