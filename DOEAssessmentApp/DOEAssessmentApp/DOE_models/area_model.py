from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=False)
    projectid = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    functionalities = db.relationship('Functionality', backref='area', cascade='all,delete')
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, nam, desc, projid):
        self.name = nam
        self.description = desc
        self.projectid = projid

    def __repr__(self):
        return '<Area %r>' % self.name
