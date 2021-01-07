from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(), nullable=False)
    projectid = db.Column(db.Integer, nullable=False)
    assessmentcompletion = db.Column(db.Numeric())
    achievedpercentage = db.Column(db.Numeric())
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, description, projectid):
        self.name = name
        self.description = description
        self.projectid = projectid

    def __repr__(self):
        return '<Area %r>' % self.name
