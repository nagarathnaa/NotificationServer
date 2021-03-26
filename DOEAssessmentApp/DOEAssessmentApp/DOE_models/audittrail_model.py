from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Audittrail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modulename = db.Column(db.String(180), nullable=False)
    operation = db.Column(db.String(10), nullable=False)
    databefore = db.Column(db.String(), nullable=False)
    dataafter = db.Column(db.String(), nullable=False)
    operationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    operatedby = db.Column(db.String(20))

    def __init__(self, modulename, operation, databefore, dataafter, operatedby):
        self.modulename = modulename
        self.operation = operation
        self.databefore = databefore
        self.dataafter = dataafter
        self.operatedby = operatedby

    def __repr__(self):
        return '<Audittrail %r>' % self.modulename
