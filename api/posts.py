import os
from flask import request, jsonify, url_for, g
from dateutil import parser
from . import api
from .decorators import verify_login
from utils import save_picture


# All the routes that require a used to be logged in, such as creating a post or getting a feed of followed user posts,
# rely on a token being sent with the request


@api.route('/post', methods=['POST'])
@verify_login
def create_post():
    from models import Post

    image_file = None
    if 'img_string' in request.json and request.json['img_string'] is not None:
        image_file = save_picture(request.json['img_string'])

    post = Post(body=request.json['body'], image_file=image_file, author_id=g.logged_in_user.id)

    from main import db
    db.session.add(post)
    db.session.commit()

    return jsonify({'post': post.to_json()}), 201


@api.route('/post', methods=['DELETE'])
@verify_login
def delete_post():
    from models import Post

    if 'post_id' not in request.json:
        return jsonify({"message": "post_id was not provided"}), 400

    post = Post.query.get_or_404(request.json['post_id'])

    if post.author_id != g.logged_in_user.id:
        return jsonify({"message": "post author_id does not match logged in user"}), 403

    from main import app
    if post.image_file and os.path.exists(os.path.join(app.root_path, 'static/images', post.image_file)):
        os.remove(os.path.join(app.root_path, 'static/images', post.image_file))

    from main import db
    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted', 'post': post.to_json()}), 200


@api.route('/public_timeline', methods=['GET'])
def get_public_timeline():
    from models import Post

    page = request.args.get('page', 1, type=int)

    query = Post.query
    if 'after' in request.headers:
        after = parser.parse(request.headers['after'])
        query = query.filter(Post.timestamp > after)

    if 'before' in request.headers:
        before = parser.parse(request.headers['before'])
        query = query.filter(Post.timestamp < before)

    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=True)

    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_public_timeline', _external=True, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_public_timeline', _external=True, page=page+1)

    return jsonify({'posts': [post.to_json() for post in posts],
                    'pagination': {'prev': prev,
                                   'next': next,
                                   'count': pagination.total}}), 200


@api.route('/<int:user_id>/private_timeline', methods=['GET'])
@verify_login
def get_private_timeline(user_id):
    from models import Post

    user = g.logged_in_user
    if user.id != user_id:
        return jsonify({"message": "user ID does not match"}), 403

    page = request.args.get('page', 1, type=int)

    query = user.followed_posts
    if 'after' in request.headers:
        after = parser.parse(request.headers['after'])
        query = query.filter(Post.timestamp > after)

    if 'before' in request.headers:
        before = parser.parse(request.headers['before'])
        query = query.filter(Post.timestamp < before)

    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=True)

    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_private_timeline', _external=True, user_id=user.id, page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_private_timeline', _external=True,  user_id=user.id, page=page + 1)

    return jsonify({'posts': [post.to_json() for post in posts],
                    'pagination': {'prev': prev,
                                   'next': next,
                                   'count': pagination.total}}), 200
