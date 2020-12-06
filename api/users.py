from flask import request, jsonify, g
from . import api
from .decorators import verify_login


@api.route('/register', methods=['POST'])
def register_user():
    from models import User

    if 'username' not in request.json:
        return jsonify({"message": "username was not provided"}), 400
    elif 'password' not in request.json:
        return jsonify({"message": "password was not provided"}), 400

    user = User.query.filter_by(username=request.json['username']).first()

    if user is None:
        try:
            user = User(username=request.json['username'], password=request.json['password'])
            from main import db
            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token()
            return jsonify({'auth_token': auth_token.decode()}), 201
        except Exception as e:
            print(e)
            return jsonify({'message': 'An error occurred. Please try again.'}), 401

    return jsonify({'message': 'Username not available'}), 409


# The server must not store any state about the client that persists from one request to the next so the user is logged
# in by the caller using the token returned by the login route

@api.route('/login', methods=['POST'])
def login_user():
    from models import User

    if 'username' not in request.json:
        return jsonify({"message": "username was not provided"}), 400
    elif 'password' not in request.json:
        return jsonify({"message": "password was not provided"}), 400

    user = User.query.filter_by(username=request.json['username']).first()

    if user is None:
        return jsonify({'message': 'Invalid username'}), 401
    elif not user.verify_password(request.json['password']):
        return jsonify({'message': 'Invalid password'}), 401

    try:
        auth_token = user.encode_auth_token()
        if auth_token:
            return jsonify({'auth_token': auth_token.decode()}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Try again'}), 500


@api.route('/follow', methods=['POST'])
@verify_login
def follow_user():
    from models import User

    if 'followed_username' not in request.json:
        return jsonify({"message": "followed_username was not provided"}), 400

    follower = g.logged_in_user
    followed = User.query.filter_by(username=request.json['followed_username']).first()

    if followed is None:
        return jsonify({'message': 'followed_username not valid'}), 404
    elif follower.is_following(followed):
        return jsonify({'message': follower.username + ' is already following ' + followed.username}), 406

    follow = follower.follow(followed)

    return jsonify({'data': follow.to_json()}), 201


# The method is DELETE because a Follow row/object is being deleted from the database

@api.route('/unfollow', methods=['DELETE'])
@verify_login
def unfollow_user():
    from models import User

    if 'followed_username' not in request.json:
        return jsonify({"message": "followed_username was not provided"}), 400

    follower = g.logged_in_user
    followed = User.query.filter_by(username=request.json['followed_username']).first()

    if followed is None:
        return jsonify({'message': 'followed_username not valid'}), 404
    elif not follower.is_following(followed):
        return jsonify({'message': follower.username + ' is already not following ' + followed.username}), 406

    follow = follower.unfollow(followed)

    return jsonify({'data': follow.to_json()}), 200
