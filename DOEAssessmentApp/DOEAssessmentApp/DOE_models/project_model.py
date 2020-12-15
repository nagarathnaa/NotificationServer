from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    areas = db.relationship('Area', backref='project', cascade='all, delete')
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, nam, desc, compid):
        self.name = nam
        self.description = desc
        self.companyid = compid

    def __repr__(self):
        return '<Project %r>' % self.name
