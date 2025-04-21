from .. import db
import uuid

class Users(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    isVerified = db.Column(db.Boolean, default=False)
    
    items = db.relationship('Item', backref='owner', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        return {
            "id": self._id,
            "username": self.username,
            "email": self.email,
        }

