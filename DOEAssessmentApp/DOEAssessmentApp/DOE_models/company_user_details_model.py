import jwt
import datetime
from DOEAssessmentApp import app, db
from sqlalchemy.sql import func


class Companyuserdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empid = db.Column(db.String(20), nullable=False)
    empname = db.Column(db.String(120), nullable=False, unique=True)
    emprole = db.Column(db.String(50), nullable=False)
    empemail = db.Column(db.String(120), nullable=False, unique=True)
    emppasswordhash = db.Column(db.String(255))
    companyid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, eid, ename, erole, email, epwd, cid):
        self.empid = eid
        self.empname = ename
        self.emprole = erole
        self.empemail = email
        self.emppasswordhash = epwd
        self.companyid = cid

    def __repr__(self):
        return '<Companyuserdetails %r>' % self.empname

    @staticmethod
    def encode_auth_token(login_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
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
