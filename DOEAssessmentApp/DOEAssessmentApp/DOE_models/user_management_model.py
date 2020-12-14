
from __init__ import db


class UserManagement(db.Model):
    __tablename__ ='user_management'
    emp_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    roll = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, emp_id, name, roll, email):
        self.emp_id = emp_id
        self.name = name
        self.roll = roll
        self.email = email

    def repr(self):
        return '<UserManagement %r>' % self.emp_id