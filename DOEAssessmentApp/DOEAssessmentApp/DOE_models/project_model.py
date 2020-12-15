from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, description, companyid):
        self.name = name
        self.description = description
        self.companyid = companyid

    def __repr__(self):
        return '<Project %r>' % self.name
