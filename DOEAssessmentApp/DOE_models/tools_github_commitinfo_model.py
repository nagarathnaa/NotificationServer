from DOEAssessmentApp import db
from sqlalchemy.sql import func


class GitCommitInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_id = db.Column(db.Integer)
    commit_id = db.Column(db.String)
    commit_date = db.Column(db.DateTime)
    message = db.Column(db.String)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, repo_id, commit_id, commit_date, message):
        self.repo_id = repo_id
        self.commit_id = commit_id
        self.commit_date = commit_date
        self.message = message

    def __repr__(self):
        return '<GitCommitInfo %r>' % self.repo_id
