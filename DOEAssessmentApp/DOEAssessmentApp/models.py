
"""
Models or rather table schemas for DOEAssessmentApp
"""

import jwt
import datetime
from DOEAssessmentApp import app, db

#following db schema will be created in different env
class Companydetails(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    companyname = db.Column(db.String(120), nullable=False, unique=True)
    registeredaddress = db.Column(db.String(255), nullable=False)
    billingaddress = db.Column(db.String(255), nullable=False)
    gstortaxnumber = db.Column(db.String(120), nullable=False, unique=True)
    registrationkey = db.Column(db.String(255), nullable=False)
    registrationkeyvalidated = db.Column(db.Integer, nullable=False, default=0)
    creationdatetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, cname, regadrs, billadrs, gst, regkey):
        self.companyname = cname
        self.registeredaddress = regadrs
        self.billingaddress = billadrs
        self.gstortaxnumber = gst
        self.registrationkey = regkey

    def __repr__(self):
        return '<Companydetails %r>' % self.companyname

class Companyadmindetails(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    adminname = db.Column(db.String(120), nullable=False, unique=True)
    adminemail = db.Column(db.String(120), nullable=False, unique=True)
    adminpasswordhash = db.Column(db.String(255), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, admname, admemail, admpwd, cid):
        self.adminname = admname
        self.adminemail = admemail
        self.adminpasswordhash = admpwd
        self.companyid = cid

    def __repr__(self):
        return '<Companyadmindetails %r>' % self.adminname

    def encode_auth_token(self, login_id):
       """
       Generates the Auth Token
       :return: string
       """
       try:
           payload = {
              'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30),
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

class Rbac(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature = db.Column(db.String(120), nullable=False, unique=True)
    roles =  db.Column(db.String(255), nullable=False)

    def __init__(self, feat, rol):
        self.feature = feat
        self.roles = rol

    def __repr__(self):
        return '<Rbac %r>' % self.feature
