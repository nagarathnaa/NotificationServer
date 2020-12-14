from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Functionality(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(), nullable=False)
    retake_assessment_days = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    subfunctionalities = db.relationship('Subfunctionality', backref='functionality', lazy=True)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, nam, desc):
        self.name = nam
        self.description = desc

    def __repr__(self):
        return '<Functionality %r>' % self.name
