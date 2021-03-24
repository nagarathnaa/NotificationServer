from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.tools_gitlab_model import GitLab
from DOEAssessmentApp.DOE_models.tools_login_model import ToolsLogin
from werkzeug.security import generate_password_hash, check_password_hash

gitlabtool = Blueprint('gitlabtool', __name__)

colstools = ['id',  'repos_id', 'repos_name', 'count_repos', 'users_name',
             'namespaces_name', 'broadcastmessages', 'groups_list', 'count_groups_list', 'issues_list',
             'count_issues_list', 'licenses_list', 'mergerequests_list', 'dockerfiles_list', 'count_dockerfiles_list',
             'gitlabciymls_list', 'count_gitlabciymls_list', 'gitlab_snippets_list', 'count_snippets_list',
             'gitlab_events_lists', 'count_events_list', 'events_created_at', 'count_events_commits']


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@gitlabtool.route('/api/getjenkinsdata', methods=['GET'])
def get_gitlab_tool_data():
    try:
        if request.method == "GET":
            data = GitLab.query.all()
            result = [{col: getattr(d, col) for col in colstools} for d in data]
            return jsonify({"data": result}), 200
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500