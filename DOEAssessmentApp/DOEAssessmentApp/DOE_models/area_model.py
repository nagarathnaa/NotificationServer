from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    functionalities = db.relationship('Functionality', backref='area', lazy=True)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, nam, desc):
        self.name = nam
        self.description = desc

    def __repr__(self):
        return '<Area %r>' % self.name
