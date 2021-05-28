from functools import wraps

from flask import request, jsonify
from .models import User

def token_required(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        token = request.headers.get('X-API-KEY')
        if not token or not User.verify_auth_token(token):
            return jsonify({
                'message': 'Invalid Token'
            }), 401
        return f(*args, **kwargs)
    return decorator_function
