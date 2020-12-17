from DOEAssessmentApp import db
from sqlalchemy.sql import func


class AddingProjectManager(db.Model):
    __tablename__ = 'adding_project_manager'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=1)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, emp_id, project_id):
        self.emp_id = emp_id
        self.project_id = project_id

    def repr(self):
        return '<AddingProjectManager %r>' % self.emp_id
