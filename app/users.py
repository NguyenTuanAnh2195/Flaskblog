from flask import (
    Blueprint
)
from flask_restful import Resource

from app import api
from app.models import User, PostSchema, UserSchema


user_bp = Blueprint('users', __name__)

class UserAPI(Resource):
    def get(self, id):
        user_schema = UserSchema()
        post_schema = PostSchema(many=True)
        
        user = User.query.get(id)
        posts = user.posts

        user = user_schema.dump(user)
        posts = post_schema.dump(posts)

        if not user:
            return { 'message': 'User not found' }, 404
        
        return {
            'user': user,
            'posts': posts
        }

api.add_resource(UserAPI, '/v1/users/<int:id>', endpoint = 'user')
