
"""
Models or rather table schemas for DOEAssessmentApp
"""

import jwt
import datetime
from DOEAssessmentApp import app, db

class Emailconfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    host = db.Column(db.String(120), nullable=False)
    passwordhash = db.Column(db.String(255), nullable=False)

    def __init__(self, emailid, hostname, password):
        self.email = emailid
        self.host = hostname
        self.passwordhash = password

    def __repr__(self):
        return '<Emailconfiguration %r>' % self.email

    def encode_auth_token(self, login_id):
       """
       Generates the Auth Token
       :return: string
       """
       try:
           payload = {
              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=2592000),
              'iat': datetime.datetime.utcnow(),
              'sub': login_id
           }
           return jwt.encode(
               payload,
               app.config.get('SECRET_KEY'),
               algorithm='HS256'
           )
       except Exception as e:
           return e

    @staticmethod
    def decode_auth_token(auth_token):
       """
       Decodes the auth token
       :param auth_token:
       :return: integer|string
       """
       try:
          payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
          return payload['sub']
       except jwt.ExpiredSignatureError:
          return 'Signature expired. Please log in again.'
       except jwt.InvalidTokenError:
          return 'Invalid token. Please log in again.'

class Rbac(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature = db.Column(db.String(120), nullable=False, unique=True)
    roles =  db.Column(db.String(255), nullable=False)

    def __init__(self, feat, rol):
        self.feature = feat
        self.roles = rol

    def __repr__(self):
        return '<Rbac %r>' % self.feature
