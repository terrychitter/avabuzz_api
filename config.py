import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask app configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "production")  # Default to 'production' if not set
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")

    # Flask-SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
