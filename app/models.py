import os
import base64
from datetime import datetime, timedelta
import os

from app import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True )
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    #checks token on request
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    #returns token back to user
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    #revoke token on timeout
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def set_pw(self,password):
        self.password_hash = generate_password_hash(password)

    def check_pw(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User {0} : {1}>'.format(str(self.id),self.name)

    #get as dict
    def to_dict(self):
        data = {
            'id':self.id,
            'name': self.name,
            'email': self.email
        }
        return data
    #write from incoming dict
    def from_dict(self, data, new_user=False,change_pw=False):
        for field in ['name','email']:
            if field in data:
                setattr(self,field,data[field])
        if new_user and 'password' in data:
            self.set_pw(data['password'])

        if change_pw and 'password' in data:
            self.set_pw(data['password'])
