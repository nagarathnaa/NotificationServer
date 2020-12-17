from DOEAssessmentApp import db
from sqlalchemy.sql import func


class AddingTeamMember(db.Model):
    __tablename__ = 'adding_team_member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(50), primary_key=True)
    projectid = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    functionality_id = db.Column(db.Integer, nullable=False)
    subfunctionality_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=1)
    combination = db.Column(db.String(50), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, emp_id, projectid, area_id, functionality_id,
                 subfunctionality_id,combination):
        self.emp_id = emp_id
        self.projectid = projectid
        self.area_id = area_id
        self.functionality_id = functionality_id
        self.subfunctionality_id = subfunctionality_id
        self.combination = combination

    def repr(self):
        return '<AddingTeamMember %r>' % self.emp_id
