from flask import g
from flask_cors import cross_origin
from flask_httpauth import HTTPBasicAuth
from app.models import User
from app.api.errors import error_response
from flask_httpauth import HTTPTokenAuth

token_auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()

@cross_origin()
@basic_auth.verify_password
def verify_password(email, password):
    print(email)
    print(password)
    user = User.query.filter_by(email=email).first()
    print(user)
    if user is None:
        return False
    g.current_user = user
    return user.check_pw(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

@cross_origin()
@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(401)