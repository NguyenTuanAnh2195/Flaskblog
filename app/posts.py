from flask import (
    Blueprint, g, request, jsonify, current_app
)
from flask_restful import Api, Resource

from app import db, api
from app.models import Post, User
from app.common import token_required


post_bp = Blueprint('posts', __name__)


class PostAPI(Resource):
    def show(self, id):
        post = Post.query.get(id)
        return { 'post': post }

    @token_required
    def post(self):
        title = request.json.get('title')
        content = request.json.get('content')
        token = request.headers.get('X-API-KEY')
        user = User.verify_auth_token(token)
        post = Post(title = title, content = content, user = user)
        db.session.add(post)
        db.session.commit()
        return { 'message': 'Success' }, 201

    @token_required
    def delete(self, id):
        post = Post.query.get(id)
        token = request.headers.get('X-API-KEY')
        user = User.verify_auth_token(token)
        if post.user_id != user.id:
            return { 'message': 'Unauthorized'}, 401
        if not post:
            return { 'message': 'Post does not exist'}, 404
        db.session.delete(post)
        db.session.commit()
        return { 'message': 'Delete Successul'}, 204


class PostListAPI(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        ).items
        return jsonify({ 'post': posts })


api.add_resource(PostAPI, '/v1/posts/<int:id>', endpoint = 'post')
api.add_resource(PostListAPI, '/v1/posts/', endpoint = 'posts')