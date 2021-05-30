from flask import (
    Blueprint, g, request, jsonify
)
from app import db
from app.models import User
from app.common import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/v1/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    password = request.json.get('password')
    email = request.json.get('email')

    if not name or not password or not email:
        return jsonify({
            'error': 400,
            'message': 'User is lacking email, name or password!'
        }), 400
    if User.query.filter_by(name=name).first() or \
            User.query.filter_by(email=email).first():
        return jsonify({
            'error': 400,
            'message': 'User already exists!'
        }), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'name': name}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    name = request.json.get('name')
    password = request.json.get('password')
    user = verify_password(name, password)
    if not user:
        return jsonify({'message': 'Invalid Login Information'}), 404
    g.user = user
    token = g.user.generate_auth_token()
    return jsonify({'message': 'success', 'token': token.decode('utf-8')})


def verify_password(name, password):
    user = User.query.filter_by(name=name).first()
    if user and user.check_password(password):
        return user
    return None


@auth_bp.route('/test', methods=['GET'])
@token_required
def test():
    return jsonify({
        'message': 'Hello World'
    })
