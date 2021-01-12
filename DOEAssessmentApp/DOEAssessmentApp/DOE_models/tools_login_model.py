from DOEAssessmentApp import db
from sqlalchemy.sql import func


class ToolsLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    url = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, name, url, password):
        self.name = name
        self.url = url
        self.password = password

    def __repr__(self):
        return '<ToolsLogin %r>' % self.name

