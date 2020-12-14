import datetime
from DOEAssessmentApp import db


class Rbac(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature = db.Column(db.String(120), nullable=False, unique=True)
    roles = db.Column(db.String(255), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, feat, rol):
        self.feature = feat
        self.roles = rol

    def __repr__(self):
        return '<Rbac %r>' % self.feature
