from flask import (
    Blueprint, g, redirect, request, url_for, abort, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import User
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth

import functools

bp = Blueprint('auth', __name__, url_prefix='/v1/auth')

@bp.route('/register')
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400)
    if User.query.filter_by(username = username).first() is not None:
        abort(400)

    user = User(username = username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}


