from DOEAssessmentApp import db
from sqlalchemy.sql import func
import sqlalchemy as sa


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    answer_type = db.Column(db.String(50), nullable=False)
    answers = db.Column(sa.ARRAY(sa.JSON), nullable=False)
    maxscore = db.Column(db.Integer, nullable=False)
    subfunc_id = db.Column(db.Integer)
    func_id = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    proj_id = db.Column(db.Integer, nullable=False)
    combination = db.Column(db.String, nullable=False)
    mandatory = db.Column(db.Integer, default=1)
    islocked = db.Column(db.Integer)
    isdependentquestion = db.Column(db.Integer, default=0)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, answer_type, answers, maxscore, subfunc_id, func_id, area_id, proj_id, combination,
                 mandatory):
        self.name = name
        self.answer_type = answer_type
        self.answers = answers
        self.maxscore = maxscore
        self.subfunc_id = subfunc_id
        self.func_id = func_id
        self.area_id = area_id
        self.proj_id = proj_id
        self.combination = combination
        self.mandatory = mandatory

    def __repr__(self):
        return '<Question %r>' % self.name
