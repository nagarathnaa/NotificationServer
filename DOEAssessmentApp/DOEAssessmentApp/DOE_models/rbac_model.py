from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(180), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(self, name, companyid):
        self.name = name
        self.companyid = companyid

    def __repr__(self):
        return '<Role %r>' % self.name


class Rbac(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature = db.Column(db.String(120), nullable=False, unique=True)
    roles = db.Column(db.String(255), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, feat, rol):
        self.feature = feat
        self.roles = rol

    def __repr__(self):
        return '<Rbac %r>' % self.feature
