from DOEAssessmentApp import db
from sqlalchemy.sql import func
import sqlalchemy as sa


class GitHub(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_id = db.Column(db.Integer, nullable=False, unique=True)
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
    branches_url = db.Column(db.String())
    branch_name = db.Column(db.String())
    branches_count = db.Column(db.String())
    brnch_commit_id = db.Column(db.String())
    branch_commit_count = db.Column(db.String())
    languages_url = db.Column(db.String())
    languages = db.Column(sa.ARRAY(sa.JSON))
    languages_count = db.Column(db.String())
    releases_url = db.Column(db.String())
    releases_url_name = db.Column(db.String())
    releases_count = db.Column(db.String())
    releases_url_published_at = db.Column(db.String())
    prerelease = db.Column(db.String())
    commits_count = db.Column(db.String())
    community_health_percentage = db.Column(db.String())
    pulls_rqs_count = db.Column(db.String())
    count_user = db.Column(db.String())
    repo_pullrqs_accpted = db.Column(db.String())
    repo_pullrqs_rejcted = db.Column(db.String())
    user_pullrqs_accpted = db.Column(db.String())
    user_pullrqs_rejcted = db.Column(db.String())
    count_repo_pullrqs = db.Column(db.String())
    count_user_pullrqs = db.Column(db.String())
    count_branch_pullrqs = db.Column(db.String())
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, repo_id, name, description, created_on, updated_on, owner, license,
                 includes_wiki,
                 forks_count, issues_count, stars_count, watchers_count, repo_url, commits_url,
                 branches_url, branch_name, branches_count, brnch_commit_id, branch_commit_count,
                 languages_url, languages, languages_count, releases_url, releases_url_name,
                 releases_count, releases_url_published_at, prerelease,
                 community_health_percentage, pulls_rqs_count, count_user,
                 count_repo_pullrqs, count_user_pullrqs, count_branch_pullrqs, repo_pullrqs_accpted,
                 repo_pullrqs_rejcted, user_pullrqs_accpted, user_pullrqs_rejcted):
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
        self.branches_url = branches_url
        self.branch_name = branch_name
        self.branches_count = branches_count
        self.brnch_commit_id = brnch_commit_id
        self.branch_commit_count = branch_commit_count
        self.languages_url = languages_url
        self.languages = languages
        self.languages_count = languages_count
        self.releases_url = releases_url
        self.releases_url_name = releases_url_name
        self.releases_count = releases_count
        self.releases_url_published_at = releases_url_published_at
        self.prerelease = prerelease
        self.community_health_percentage = community_health_percentage
        self.pulls_rqs_count = pulls_rqs_count
        self.count_user = count_user
        self.repo_pullrqs_accpted = repo_pullrqs_accpted
        self.repo_pullrqs_rejcted = repo_pullrqs_rejcted
        self.user_pullrqs_accpted = user_pullrqs_accpted
        self.user_pullrqs_rejcted = user_pullrqs_rejcted
        self.count_repo_pullrqs = count_repo_pullrqs
        self.count_user_pullrqs = count_user_pullrqs
        self.count_branch_pullrqs = count_branch_pullrqs

    def __repr__(self):
        return '<GitHub %r>' % self.name


db.create_all()
