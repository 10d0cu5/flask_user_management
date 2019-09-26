from flask import jsonify
from flask import request
from flask import url_for
from flask import g, abort
from flask_cors import cross_origin

from app.api.auth import token_auth
from app import db
from app.api import bp
from app.api.errors import bad_request,not_found
from app.models import User

@bp.route('/users/<int:id>', methods=['GET','DELETE'])
@token_auth.login_required
def get_user(id):
    if request.method == 'GET':
        data = User.query.get_or_404(id).to_dict()
        if data == {} or data == None:
            return not_found("User not found!")

        return jsonify(user=data),200
    elif request.method == 'DELETE':
        data = User.query.get_or_404(id).to_dict()
        if data == {} or data == None:
            return not_found("User not found!")

        db.session.remove(data)
        db.session.commit()

        return 200


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    users = User.query.all()
    if users == None:
        return not_found("Users not found!")
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

    return jsonify(users=user_list), 200




@bp.route('/users', methods=['POST'])
@cross_origin()
def create_user():
    data = request.get_json() or {}
    if 'name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include name, email and password fields')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()

    id = len(User.query.all())
    print(id)

    if 'id' not in data:
        data['id'] = id

    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code=201
    response.headers['Location'] = url_for('api.get_user',id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email')

    change_pw = False
    if 'password' in data:
        change_pw = True

    user.from_dict(data,change_pw)
    db.session.commit()
    return jsonify(user.to_dict())

