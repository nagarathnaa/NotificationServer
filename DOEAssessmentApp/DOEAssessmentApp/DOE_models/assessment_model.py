from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(50), nullable=False)
    projectid = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    functionality_id = db.Column(db.Integer, nullable=False)
    subfunctionality_id = db.Column(db.Integer)
    employeeassignedstatus = db.Column(db.Integer, default=1)
    combination = db.Column(db.String(50), nullable=False)
    totalmaxscore = db.Column(db.Integer)
    totalscoreachieved = db.Column(db.Integer)
    countoftotalquestions = db.Column(db.Integer)
    comment = db.Column(db.String(180))
    assessmentstatus = db.Column(db.String(50), nullable=False)
    assessmenttakendatetime = db.Column(db.DateTime)
    assessmentrevieweddatetime = db.Column(db.DateTime)
    assessmentretakedatetime = db.Column(db.DateTime)
    active = db.Column(db.Integer, default=1)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, emp_id, projectid, area_id, functionality_id, subfunctionality_id,
                 combination, assessmentstatus, countoftotalquestions):
        self.emp_id = emp_id
        self.projectid = projectid
        self.area_id = area_id
        self.functionality_id = functionality_id
        self.subfunctionality_id = subfunctionality_id
        self.combination = combination
        self.assessmentstatus = assessmentstatus
        self.countoftotalquestions = countoftotalquestions

    def repr(self):
        return '<Assessment %r>' % self.id
