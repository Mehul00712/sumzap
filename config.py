import os
from dotenv import load_dotenv

# Check if the secret file exists in Render's secret path
secret_path = '/etc/secrets/.env'
if os.path.exists(secret_path):
    load_dotenv(secret_path)
else:
    # Fall back to local .env file for development
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-for-dev'
    
    # Check if running on Render
    if os.environ.get('RENDER'):
        # Use in-memory SQLite for Render's free tier
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sumzap.db'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Use a directory that's accessible on Render
    if os.environ.get('RENDER'):
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp/uploads')
    else:
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
        
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')