from flask import Blueprint

bp = Blueprint('api_v1', __name__)

from app.api.v1 import welcome, users, posts

# Register the blueprints with the main api_v1 blueprint
bp.register_blueprint(welcome.bp)
bp.register_blueprint(users.bp)
bp.register_blueprint(posts.bp)
