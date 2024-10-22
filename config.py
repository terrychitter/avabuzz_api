import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask app configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "production")  # Default to 'production' if not set
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")

    # API KEY
    API_KEY:str = os.getenv("API_KEY", "your_default_api_key")

    # Flask-SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URI", "sqlite:///default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # JWT configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_default_jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = 2592000 # 30 days
    JWT_BLACKLIST_ENABLED: bool = True
    JWT_BLACKLIST_TOKEN_CHECKS: list = ["access", "refresh"]
