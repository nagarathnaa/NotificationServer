from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    assessmentcompletion = db.Column(db.Integer)
    achievedpercentage = db.Column(db.Numeric(3, 2))
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, description, companyid):
        self.name = name
        self.description = description
        self.companyid = companyid

    def __repr__(self):
        return '<Project %r>' % self.name


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    range_from = db.Column(db.Integer, nullable=False)
    range_to = db.Column(db.Integer, nullable=False)
    combination = db.Column(db.String(50), unique=True, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, range_from, range_to, combo, project_id):
        self.name = name
        self.range_from = range_from
        self.range_to = range_to
        self.combination = combo
        self.project_id = project_id

    def __repr__(self):
        return '<Level %r>' % self.name
