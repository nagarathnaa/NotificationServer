from DOEAssessmentApp import db
from sqlalchemy.sql import func
import sqlalchemy as sa


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(), nullable=False)
    levels = db.Column(sa.ARRAY(sa.JSON), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    assessmentcompletion = db.Column(db.Numeric())
    achievedpercentage = db.Column(db.Numeric())
    achievedlevel = db.Column(db.String(2))
    needforreview = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, name, description, levels, companyid, needforreview, createdby):
        self.name = name
        self.description = description
        self.levels = levels
        self.companyid = companyid
        self.needforreview = needforreview
        self.createdby = createdby

    def __repr__(self):
        return '<Project %r>' % self.name
