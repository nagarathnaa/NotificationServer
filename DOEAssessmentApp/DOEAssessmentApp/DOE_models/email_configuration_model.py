import datetime
from DOEAssessmentApp import db


class Emailconfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    host = db.Column(db.String(120), nullable=False)
    passwordhash = db.Column(db.String(255), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, emailid, hostname, password):
        self.email = emailid
        self.host = hostname
        self.passwordhash = password

    def __repr__(self):
        return '<Emailconfiguration %r>' % self.email
