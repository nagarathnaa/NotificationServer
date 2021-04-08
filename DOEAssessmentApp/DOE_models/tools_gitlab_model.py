from DOEAssessmentApp import db
from sqlalchemy.sql import func
import sqlalchemy as sa


class GitLab(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repos_id = db.Column(db.Integer, nullable=False, unique=True)
    repos_name = db.Column(db.String(180), nullable=False)
    count_repos = db.Column(db.String(180))
    users_name = db.Column(db.String(180))
    namespaces_name = db.Column(db.String(180))
    broadcastmessages = db.Column(db.String(180))
    groups_list = db.Column(db.String(180))
    count_groups_list = db.Column(db.String(180))
    issues_list = db.Column(db.String(180))
    count_issues_list = db.Column(db.String(180))
    licenses_list = db.Column(db.String(180))
    mergerequests_list = db.Column(db.String(180))
    dockerfiles_list = db.Column(db.String(180))
    count_dockerfiles_list = db.Column(db.String(180))
    gitlabciymls_list = db.Column(db.String(180))
    count_gitlabciymls_list = db.Column(db.String(180))
    gitlab_snippets_list = db.Column(db.String(180))
    count_snippets_list = db.Column(db.String(180))
    gitlab_events_lists = db.Column(db.String(180))
    count_events_list = db.Column(db.String(180))
    events_created_at = db.Column(db.String(180))
    count_events_commits = db.Column(db.String(180))
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, repos_id, repos_name, count_repos, users_name,
             namespaces_name, broadcastmessages, groups_list, count_groups_list, issues_list,
             count_issues_list, licenses_list, mergerequests_list, dockerfiles_list, count_dockerfiles_list,
             gitlabciymls_list, count_gitlabciymls_list, gitlab_snippets_list, count_snippets_list,
             gitlab_events_lists, count_events_list, events_created_at, count_events_commits):
        self.repos_id = repos_id
        self.repos_name = repos_name
        self.count_repos = count_repos
        self.users_name = users_name
        self.namespaces_name = namespaces_name
        self.broadcastmessages = broadcastmessages
        self.groups_list = groups_list
        self.count_groups_list = count_groups_list
        self.issues_list = issues_list
        self.count_issues_list = count_issues_list
        self.licenses_list = licenses_list
        self.mergerequests_list = mergerequests_list
        self.dockerfiles_list = dockerfiles_list
        self.count_dockerfiles_list = count_dockerfiles_list
        self.gitlabciymls_list = gitlabciymls_list
        self.count_gitlabciymls_list = count_gitlabciymls_list
        self.gitlab_snippets_list = gitlab_snippets_list
        self.count_snippets_list = count_snippets_list
        self.gitlab_events_lists = gitlab_events_lists
        self.count_events_list = count_events_list
        self.events_created_at = events_created_at
        self.count_events_commits = count_events_commits

    def __repr__(self):
        return '<GitLab %r>' % self.name


db.create_all()
