from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receiver = db.Column(db.String(255), nullable=False)
    event_name = db.Column(db.String(255), nullable=False, unique=True)
    mail_subject = db.Column(db.String(255), nullable=False)
    mail_body = db.Column(db.String(255), nullable=False)
    app_notif_body = db.Column(db.String(255), nullable=False)
    companyid = db.Column(db.Integer, nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, receiver, event_name, mail_subject, mail_body, app_notif_body, companyid, createdby):
        self.receiver = receiver
        self.event_name = event_name
        self.mail_subject = mail_subject
        self.mail_body = mail_body
        self.app_notif_body = app_notif_body
        self.companyid = companyid
        self.createdby = createdby

    def __repr__(self):
        return '<Notification %r>' % self.receiver
