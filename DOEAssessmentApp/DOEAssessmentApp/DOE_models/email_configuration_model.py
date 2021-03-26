from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Emailconfiguration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    host = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, email, host, password, companyid, createdby):
        self.email = email
        self.host = host
        self.password = password
        self.companyid = companyid
        self.createdby = createdby

    def __repr__(self):
        return '<Emailconfiguration %r>' % self.email
