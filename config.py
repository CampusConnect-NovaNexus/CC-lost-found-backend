import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 days
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Fixed variable name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
