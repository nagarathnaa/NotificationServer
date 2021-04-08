from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name = db.Column(db.String(255), nullable=False)
    total_no_build = db.Column(db.String(50))
    total_no_success = db.Column(db.String(50))
    total_no_failure = db.Column(db.String(50))
    lastBuild_number = db.Column(db.String(50))
    lastBuild_duration = db.Column(db.String(50))
    lastBuild_user = db.Column(db.String(100))
    lastBuild_result = db.Column(db.String(50))
    lastCompletedBuild_number = db.Column(db.String(50))
    lastCompletedBuild_duration = db.Column(db.String(50))
    lastCompletedBuild_user = db.Column(db.String(100))
    lastFailedBuild_number = db.Column(db.String(50))
    lastFailedBuild_duration = db.Column(db.String(50))
    lastFailedBuild_user = db.Column(db.String(100))
    lastStableBuild_number = db.Column(db.String(50))
    lastStableBuild_duration = db.Column(db.String(50))
    lastSuccessfulBuild_number = db.Column(db.String(50))
    lastSuccessfulBuild_duration = db.Column(db.String(50))
    lastUnstableBuild = db.Column(db.String(50))
    healthReport_score = db.Column(db.String(50))
    lastUnsuccessfulBuild_number = db.Column(db.String(50))
    lastUnsuccessfulBuild_duration = db.Column(db.String(50))
    lastUnsuccessfulBuild_user = db.Column(db.String(100))
    lastSuccessfulBuild_user = db.Column(db.String(100))
    lastStableBuild_user = db.Column(db.String(100))
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, job_name, total_no_build, total_no_success, total_no_failure, lastBuild_number,
                 lastBuild_duration, lastBuild_user, lastBuild_result, lastCompletedBuild_number,
                 lastCompletedBuild_duration, lastCompletedBuild_user, lastFailedBuild_number, lastFailedBuild_duration,
                 lastFailedBuild_user, lastStableBuild_number, lastStableBuild_duration, lastSuccessfulBuild_number,
                 lastSuccessfulBuild_duration, lastUnstableBuild, healthReport_score, lastUnsuccessfulBuild_number,
                 lastUnsuccessfulBuild_duration, lastUnsuccessfulBuild_user, lastSuccessfulBuild_user,
                 lastStableBuild_user):
        self.job_name = job_name
        self.total_no_build = total_no_build
        self.total_no_success = total_no_success
        self.total_no_failure = total_no_failure
        self.lastBuild_number = lastBuild_number
        self.lastBuild_duration = lastBuild_duration
        self.lastBuild_user = lastBuild_user
        self.lastBuild_result = lastBuild_result
        self.lastCompletedBuild_number = lastCompletedBuild_number
        self.lastCompletedBuild_duration = lastCompletedBuild_duration
        self.lastCompletedBuild_user = lastCompletedBuild_user
        self.lastFailedBuild_number = lastFailedBuild_number
        self.lastFailedBuild_duration = lastFailedBuild_duration
        self.lastFailedBuild_user = lastFailedBuild_user
        self.lastStableBuild_number = lastStableBuild_number
        self.lastStableBuild_duration = lastStableBuild_duration
        self.lastSuccessfulBuild_number = lastSuccessfulBuild_number
        self.lastSuccessfulBuild_duration = lastSuccessfulBuild_duration
        self.lastUnstableBuild = lastUnstableBuild
        self.healthReport_score = healthReport_score
        self.lastUnsuccessfulBuild_number = lastUnsuccessfulBuild_number
        self.lastUnsuccessfulBuild_duration = lastUnsuccessfulBuild_duration
        self.lastUnsuccessfulBuild_user = lastUnsuccessfulBuild_user
        self.lastSuccessfulBuild_user = lastSuccessfulBuild_user
        self.lastStableBuild_user = lastStableBuild_user

    def __repr__(self):
        return '<Tools %r>' % self.name
