import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS 

# Create SQLAlchemy and Migrate instances
db = SQLAlchemy()


def create_app(config_class=Config):
    # Create a Flask application
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    from app.services.jwt import jwt
    jwt.init_app(app)

    # Initialize SQLAlchemy
    db.init_app(app)
    # Initialize Migrate
    migrate = Migrate(app, db)

    # Register blueprints
    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")


    # Custom error handlers
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({"error": "Method Not Allowed"}), 405

    @app.errorhandler(415)
    def unsupported_media_type_error(error):
        return jsonify({"error": "Unsupported Media Type"}), 415

    @app.errorhandler(500)
    def internal_server_error(error):
        print(f"Internal Server Error: {str(error)}")
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    return app
