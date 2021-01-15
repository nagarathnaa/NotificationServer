import requests
from requests.auth import HTTPBasicAuth

from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.tools_github_repoinfo_model import Git
from DOEAssessmentApp.DOE_models.tools_login_model import ToolsLogin
from werkzeug.security import generate_password_hash, check_password_hash

gits = Blueprint('gits', __name__)

colsgits = ['id', 'repo_id', 'name', 'description', 'created_on', 'updated_on', 'owner', 'license', 'includes_wiki',
            'forks_count', 'issues_count', 'stars_count', 'watchers_count', 'repo_url', 'commits_url', 'languages_url']


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@gits.route('/api/getgitdata', methods=['GET'])
def getgitdata():
    try:
        if request.method == "GET":
            data = Git.query.all()
            result = [{col: getattr(d, col) for col in colsgits} for d in data]
            return jsonify({"data": result}), 200
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@gits.route('/api/storegitdata', methods=['POST'])
def storegitdata():
    try:
        if request.method == "POST":
            result = request.get_json(force=True)
            user_name = result['name']
            user_password = result['password']
            projectid = result['projectid']
            data = ToolsLogin.query.filter(ToolsLogin.name == user_name, ToolsLogin.projectid == projectid)
            if user_name and check_password_hash(data.first().password, user_password):
                data = requests.get('https://api.github.com/users/' + user_name)
                datas = data.json()

                print("Information about user {}:\n".format(user_name))
                print("Name: {}".format(datas['name']))
                print("Email: {}".format(datas['email']))
                print("Location: {}".format(datas['location']))
                print("Public repos: {}".format(datas['public_repos']))
                print("Public gists: {}".format(datas['public_gists']))
                print("About: {}\n".format(datas['bio']))

                print("Collecting repositories information")
                url = datas['repos_url']
                page_no = 1
                repos_data = []
                while (True):
                    response = requests.get(url)
                    response = response.json()
                    repos_data = repos_data + response
                    repos_fetched = len(response)
                    print("Total repositories fetched: {}".format(repos_fetched))
                    if (repos_fetched == 30):
                        page_no = page_no + 1
                        url = datas['repos_url'] + '?page=' + str(page_no)
                    else:
                        break

                # repos_information = []
                for i, repo in enumerate(repos_data):
                    data = []
                    json_data = {}
                    data.append({"repo_id": repo['id']})
                    data.append({"name": repo['name']})
                    data.append({"description": repo['description']})
                    data.append({"created_on": repo['created_at']})
                    data.append({"updated_on": repo['updated_at']})
                    data.append({"owner": repo['owner']['login']})
                    data.append({"license": repo['license']['name'] if repo['license'] != None else None})
                    data.append({"includes_wiki": repo['has_wiki']})
                    data.append({"forks_count": repo['forks_count']})
                    data.append({"issues_count": repo['open_issues_count']})
                    data.append({"stars_count": repo['stargazers_count']})
                    data.append({"watchers_count": repo['watchers_count']})
                    data.append({"repo_url": repo['url']})
                    data.append({"commits_url": repo['commits_url'].split("{")[0]})
                    data.append({"languages_url": repo['url'] + '/languages'})
                    for i in data:
                        json_data.update(i)
                    print("update json_data", json_data)
                    repos_information = mergedict(json_data)
                    print("repos_information", repos_information)

                    repo_id = repos_information['repo_id']
                    name = repos_information['name']
                    description = repos_information['description']
                    created_on = repos_information['created_on']
                    updated_on = repos_information['updated_on']
                    owner = repos_information['owner']
                    license = repos_information['license']
                    includes_wiki = repos_information['includes_wiki']
                    forks_count = repos_information['forks_count']
                    issues_count = repos_information['issues_count']
                    stars_count = repos_information['stars_count']
                    watchers_count = repos_information['watchers_count']
                    repo_url = repos_information['repo_url']
                    commits_url = repos_information['commits_url']
                    languages_url = repos_information['languages_url']
                    json_datas = Git(repo_id, name, description, created_on, updated_on, owner, license, includes_wiki,
                                     forks_count, issues_count, stars_count, watchers_count, repo_url, commits_url,
                                     languages_url)
                    db.session.add(json_datas)
                    db.session.commit()

            return make_response(jsonify({"msg": f"GitHub data successfully inserted."})), 201
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
