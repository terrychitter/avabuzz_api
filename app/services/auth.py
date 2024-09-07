import os
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def api_key_required(f):
    """
    Decorator to check for the presence of a valid API key in the request headers

    Args:
        f (function): The function to decorate

    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key != os.getenv("API_KEY"):
            return jsonify({"message": "Forbidden or Invalid API key"}), 403
        return f(*args, **kwargs)

    return decorated_function
