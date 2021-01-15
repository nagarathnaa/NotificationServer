from DOEAssessmentApp import db
from sqlalchemy.sql import func


class Git(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_id = db.Column(db.Integer)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String())
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    owner = db.Column(db.String())
    license = db.Column(db.String())
    includes_wiki = db.Column(db.String())
    forks_count = db.Column(db.String())
    issues_count = db.Column(db.String())
    stars_count = db.Column(db.String())
    watchers_count = db.Column(db.String())
    repo_url = db.Column(db.String())
    commits_url = db.Column(db.String())
    languages_url = db.Column(db.String())
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, repo_id, name, description, created_on, updated_on, owner, license, includes_wiki, forks_count,
                 issues_count, stars_count, watchers_count, repo_url,commits_url, languages_url):
        self.repo_id = repo_id
        self.name = name
        self.description = description
        self.created_on = created_on
        self.updated_on = updated_on
        self.owner = owner
        self.license = license
        self.includes_wiki = includes_wiki
        self.forks_count = forks_count
        self.issues_count = issues_count
        self.stars_count = stars_count
        self.watchers_count = watchers_count
        self.repo_url = repo_url
        self.commits_url = commits_url
        self.languages_url = languages_url

    def __repr__(self):
        return '<Area %r>' % self.name
