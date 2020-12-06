from flask import Blueprint, request

api = Blueprint('api', __name__)


@api.after_request
def after_request(response):
    if 'auth_token' not in request.headers:
        return response
    else:
        from models import User
        id = User.decode_auth_token(request.headers['auth_token'])
        user = User.query.get(id)
        response.headers['auth_token'] = user.encode_auth_token()
        return response


from . import posts, users

