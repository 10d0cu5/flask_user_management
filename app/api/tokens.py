from flask import jsonify, g, request
from flask_cors import cross_origin

from app import db
from app.api import bp
from app.api.auth import basic_auth
from app.api.auth import token_auth

@bp.route('/tokens', methods=['POST'])
@cross_origin(supports_credentials=True)
@basic_auth.login_required
def get_token():
    print(request)
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204

