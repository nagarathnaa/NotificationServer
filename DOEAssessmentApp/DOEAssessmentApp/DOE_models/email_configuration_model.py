from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Emailconfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    host = db.Column(db.String(120), nullable=False)
    passwordhash = db.Column(db.String(255), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, emailid, hostname, password):
        self.email = emailid
        self.host = hostname
        self.passwordhash = password

    def __repr__(self):
        return '<Emailconfiguration %r>' % self.email
