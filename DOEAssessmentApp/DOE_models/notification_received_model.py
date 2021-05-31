from DOEAssessmentApp import db
from sqlalchemy.sql import func


class NotificationReceived(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empid = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, default=0)
    notification_content = db.Column(db.String(300), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, empid, notification_content, createdby):
        self.empid = empid
        self.notification_content = notification_content
        self.createdby = createdby

    def __repr__(self):
        return '<NotificationReceived %r>' % self.empid
