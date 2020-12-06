from flask import request, jsonify, g
from functools import wraps


def verify_login(f):
    @wraps(f)
    def test_auth_token(*args, **kwargs):
        from models import User
        if 'auth_token' not in request.headers:
            return jsonify({'message': 'auth_token needs to be set in the header'})
        id = User.decode_auth_token(request.headers['auth_token'])
        g.logged_in_user = User.query.get_or_404(id)
        return f(*args, **kwargs)

    return test_auth_token
