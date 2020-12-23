from DOEAssessmentApp import db
from sqlalchemy.sql import func
import sqlalchemy as sa


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(50), primary_key=True)
    projectid = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    functionality_id = db.Column(db.Integer, nullable=False)
    subfunctionality_id = db.Column(db.Integer)
    totalscoreacheived = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(180), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, emp_id, projectid, area_id, functionality_id,
                 subfunctionality_id, status):
        self.emp_id = emp_id
        self.projectid = projectid
        self.area_id = area_id
        self.functionality_id = functionality_id
        self.subfunctionality_id = subfunctionality_id
        self.status = status

    def repr(self):
        return '<Assessment %r>' % self.id


class QuestionsAnswered(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qid = db.Column(db.Integer, nullable=False)
    chosenanswers = db.Column(sa.ARRAY(sa.JSON), nullable=False)
    totalscoreacheived = db.Column(db.Integer, nullable=False)
    assessmentid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, qid, chosenanswers, totalscoreacheived, assessmentid):
        self.qid = qid
        self.chosenanswers = chosenanswers
        self.totalscoreacheived = totalscoreacheived
        self.assessmentid = assessmentid

    def repr(self):
        return '<QuestionsAnswered %r>' % self.id
