from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Functionality(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(), nullable=False)
    retake_assessment_days = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    proj_id = db.Column(db.Integer, nullable=False)
    assessmentcompletion = db.Column(db.Numeric(3, 2))
    achievedpercentage = db.Column(db.Numeric(3, 2))
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, description, retake_assessment_days, area_id, proj_id):
        self.name = name
        self.description = description
        self.retake_assessment_days = retake_assessment_days
        self.area_id = area_id
        self.proj_id = proj_id

    def __repr__(self):
        return '<Functionality %r>' % self.name
