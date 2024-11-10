import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aabbccddeeffgg')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:////var/lib/docker/volumes/reporter-data/reporter-data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 80))  # Ensure port is an integer
    