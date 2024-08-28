from functools import wraps
from flask import request, jsonify

# Define your API key
VALID_API_KEY = "12345678"


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key != VALID_API_KEY:
            return jsonify({"message": "Forbidden, invalid API key"}), 403
        return f(*args, **kwargs)

    return decorated_function
