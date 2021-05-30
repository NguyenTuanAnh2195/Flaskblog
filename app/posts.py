from flask import (
    Blueprint, request, jsonify, current_app
)
from flask_restful import Resource

from app import db, api
from app.models import Post, User, Like
from app.schemas import PostSchema, LikeSchema
from app.common import token_required


post_bp = Blueprint('posts', __name__)


class PostAPI(Resource):
    def get(self, id):
        post_schema = PostSchema()
        post = Post.query.get(id)
        post = post_schema.dump(post)
        return {'post': post}

    @token_required
    def post(self):
        title = request.json.get('title')
        content = request.json.get('content')
        token = request.headers.get('X-API-KEY')
        user = User.verify_auth_token(token)
        post = Post(title=title, content=content, user=user)
        db.session.add(post)
        db.session.commit()
        return {'message': 'Success'}, 201

    @token_required
    def delete(self, id):
        post = Post.query.get(id)
        token = request.headers.get('X-API-KEY')
        user = User.verify_auth_token(token)
        if post.user_id != user.id:
            return {'message': 'Unauthorized'}, 401
        if not post:
            return {'message': 'Post does not exist'}, 404
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Delete Successul'}, 204


class PostListAPI(Resource):
    def get(self):
        posts_schema = PostSchema(many=True)
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        ).items
        posts = posts_schema.dump(posts)
        return jsonify({'post': posts})


@token_required
@post_bp.route('/v1/posts/like/<int:id>', methods=['POST'])
def like(id):
    post = Post.query.get(id)
    token = request.headers.get('X-API-KEY')
    user = User.verify_auth_token(token)
    if not post:
        return {'message': 'Post does not exist'}, 404
    like = Like.query.filter_by(post=post, user=user).first()

    # Unlike
    if like:
        db.session.delete(like)
        db.session.commit()
        return {'message': 'Unliked Post!'}

    # Add Like
    like = Like(post=post, user=user)
    db.session.add(like)
    db.session.commit()
    return {'message': 'Liked Post!'}


@post_bp.route('/v1/posts/lazylike/<int:id>', methods=['POST'])
def see_lazy_likes(id):
    post = Post.query.get(id)
    like_schema = LikeSchema(many=True)
    if not post:
        return {'message': 'Post does not exist'}, 404
    count = Like.query.filter_by(post=post).count()
    lazy_count = count
    message = ''
    if count > 3:
        lazy_count -= 2
        likes = Like.query.filter_by(post=post).limit(2).all()
        names = [like.user.name for like in likes]
        message = f"{', '.join(names)} and" + \
                  f" {count - lazy_count} other people liked this"
    else:
        likes = post.likes

    likes = like_schema.dump(likes)
    return {
        'like_count': count,
        'likers': likes,
        'lazy_count': lazy_count,
        'message': message
    }


@post_bp.route('/v1/posts/likes/<int:id>', methods=['POST'])
def see_all_likes(id):
    post = Post.query.get(id)
    like_schema = LikeSchema(many=True)
    if not post:
        return {'message': 'Post does not exist'}, 404
    likes = post.likes
    likes = like_schema.dump(likes)
    return {'likes': likes}


api.add_resource(PostAPI, '/v1/posts/<int:id>', endpoint='post')
api.add_resource(PostListAPI, '/v1/posts/', endpoint='posts')
