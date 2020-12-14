from __init__ import db


class AddingTeamMember(db.Model):
    __tablename__ = 'adding_team_member'
    emp_code = db.Column(db.String(50), primary_key=True)
    enter_team_member_name = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
    area_name = db.Column(db.String(100))
    roll = db.Column(db.String(100))
    functionality_name = db.Column(db.String(100))
    subfunctionality_name = db.Column(db.String(100))
    email_id = db.Column(db.String(100))

    def __init__(self, emp_code, enter_team_member_name, project_name, area_name, roll, functionality_name,
                 subfunctionality_name, email_id):
        self.emp_code = emp_code
        self.enter_team_member_name = enter_team_member_name
        self.project_name = project_name
        self.area_name = area_name
        self.roll = roll
        self.email_id = email_id
        self.functionality_name = functionality_name
        self.subfunctionality_name = subfunctionality_name

    def repr(self):
        return '<AddingTeamMember %r>' % self.emp_code
