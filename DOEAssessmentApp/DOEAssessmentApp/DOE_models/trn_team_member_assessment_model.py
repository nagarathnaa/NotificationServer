from DOEAssessmentApp import db
from sqlalchemy.sql import func
import sqlalchemy as sa


class QuestionsAnswered(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qid = db.Column(db.Integer, nullable=False)
    applicability = db.Column(db.Integer)
    answers = db.Column(sa.ARRAY(sa.JSON), nullable=False)
    scoreachieved = db.Column(db.Integer, nullable=False)
    maxscore = db.Column(db.Integer, nullable=False)
    assignmentid = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(180))
    active = db.Column(db.Integer, nullable=False, default=1)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, qid, applicability, answers, scoreachieved, maxscore, assignmentid, comment,
                 createdby):
        self.qid = qid
        self.applicability = applicability
        self.answers = answers
        self.scoreachieved = scoreachieved
        self.maxscore = maxscore
        self.assignmentid = assignmentid
        self.comment = comment
        self.createdby = createdby

    def repr(self):
        return '<QuestionsAnswered %r>' % self.id
