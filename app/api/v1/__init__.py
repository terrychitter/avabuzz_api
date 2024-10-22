from flask import Blueprint

bp = Blueprint('api_v1', __name__)

from app.api.v1 import debug, auth, welcome, users, posts, hashtags, blocks

# Register the blueprints with the main api_v1 blueprint
bp.register_blueprint(debug.bp)
bp.register_blueprint(auth.bp)
bp.register_blueprint(welcome.bp)
bp.register_blueprint(users.bp)
bp.register_blueprint(posts.bp)
bp.register_blueprint(hashtags.bp)
bp.register_blueprint(blocks.bp)