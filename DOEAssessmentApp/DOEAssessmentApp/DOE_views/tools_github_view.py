import requests
from requests.auth import HTTPBasicAuth

from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.tools_github_repoinfo_model import GitHub
from DOEAssessmentApp.DOE_models.tools_github_commitinfo_model import GitCommitInfo
from DOEAssessmentApp.DOE_models.tools_login_model import ToolsLogin
from werkzeug.security import generate_password_hash, check_password_hash

gits = Blueprint('gits', __name__)

colsgits = ['id', 'repo_id', 'name', 'description', 'created_on', 'updated_on', 'owner', 'license', 'includes_wiki',
            'forks_count', 'issues_count', 'stars_count', 'watchers_count', 'repo_url', 'commits_url', 'languages_url',
            'languages',
            'languages_count']


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@gits.route('/api/getgitdata', methods=['GET'])
def getgitdata():
    try:
        if request.method == "GET":
            data = GitHub.query.all()
            result = [{col: getattr(d, col) for col in colsgits} for d in data]
            return jsonify({"data": result}), 200
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@gits.route('/api/storegithubdata', methods=['POST'])
def storegithubdata():
    try:
        if request.method == "POST":
            result = request.get_json(force=True)
            user_name = result['name']
            user_password = result['password']
            projectid = result['projectid']
            git_url = result['url']
            data = ToolsLogin.query.filter(ToolsLogin.name == user_name, ToolsLogin.projectid == projectid)
            if user_name and check_password_hash(data.first().password, user_password):
                data = requests.get(git_url + user_name)
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
                print("--------response of repos_url-------------", url)
                page_no = 1
                repos_data = []
                while (True):
                    response = requests.get(url)
                    response = response.json()
                    print("--------response-------------", response)
                    repos_data = repos_data + response
                    repos_fetched = len(response)
                    print("Total repositories fetched: {}".format(repos_fetched))
                    if (repos_fetched == 30):
                        page_no = page_no + 1
                        url = datas['repos_url'] + '?page=' + str(page_no)
                    else:
                        break

                for i, repo in enumerate(repos_data):
                    data = []
                    json_data = {}
                    data.append({"repo_id": repo['id']})
                    data.append({"name": repo['name']})
                    data.append({"default_branch": repo['default_branch']})
                    data.append({"description": repo['description']})
                    data.append({"created_on": repo['created_at']})
                    data.append({"updated_on": repo['updated_at']})
                    data.append({"pushed_on": repo['pushed_at']})
                    data.append({"owner": repo['owner']['login']})
                    data.append({"license": repo['license']['name'] if repo['license'] != None else None})
                    data.append({"includes_wiki": repo['has_wiki']})
                    data.append({"forks_count": repo['forks_count']})
                    data.append({"issues_count": repo['open_issues_count']})
                    data.append({"stars_count": repo['stargazers_count']})
                    data.append({"watchers_count": repo['watchers_count']})
                    data.append({"repo_url": repo['url']})
                    data.append({"merges_url": repo['merges_url']})
                    data.append({"deployments_url": repo['deployments_url']})
                    data.append({"clone_url": repo['clone_url']})
                    data.append({"teams_url": repo['teams_url']})
                    data.append({"commits_url": repo['commits_url'].split("{")[0]})
                    data.append({"branches_url": repo['branches_url'].split("{")[0]})
                    data.append({"assignees_url": repo['assignees_url'].split("{")[0]})
                    data.append({"compare_url": repo['compare_url'].split("{")[0]})
                    data.append({"pulls_url": repo['pulls_url'].split("{")[0]})
                    data.append({"releases_url": repo['releases_url'].split("{")[0]})
                    data.append({"languages_url": repo['url'] + '/languages'})
                    data.append({"community": repo['url'] + '/community/profile'})
                    data.append({"pulls": repo['url'] + '/pulls'})
                    data.append({"pulls_url": repo['pulls_url'].split("{")[0] + '/reviews'})
                    data.append({"repo_pulls_url": repo['pulls_url'].split("{")[0]})
                    data.append({"user_pullrs": repo['url'] + '/pulls'})
                    data.append({"branch_url": repo['url'] + '/branches'})
                    for i in data:
                        json_data.update(i)
                    print("---------------------")
                    print("Collecting number of user present")
                    repo_json = {}

                    for urls in json_data.keys():
                        if urls == 'repo_url':
                            repo_url = json_data['repo_url']
                            responses = requests.get(repo_url)
                            response = responses.json()

                            if response is None or len(response) == 0:
                                check_type = ""
                                count_check_type = 0
                                repo_json = {"count_check_type": count_check_type}
                            else:
                                if response != {}:
                                    if 'owner' in response:
                                        check_type = response['owner']['type']
                                        count_check_type = 0
                                        if check_type == 'User':
                                            count_check_type = count_check_type + 1
                                            repo_json = {"count_num_of_user": count_check_type}
                                    else:
                                        check_type = ""
                                        count_check_type = 0
                                        repo_json = {"count_num_of_user": count_check_type}

                    print("---------------------")
                    print("Collecting repo pull_rs data")
                    pulls_json = {}

                    for urls in json_data.keys():
                        if urls == 'pulls':
                            pulls = json_data['pulls']
                            responses = requests.get(pulls)
                            response = responses.json()
                            print("============pulls============", response)
                            if response is None or len(response) == 0:
                                pulls_rqs_count = 0
                                pulls_json = {"repo_pulls_rqs_count": pulls_rqs_count}
                            else:
                                if response != {}:
                                    if 'message' in response:
                                        pulls_rqs_count = 0
                                        pulls_json = {"repo_pulls_rqs_count": pulls_rqs_count}
                                    else:
                                        pull_rs = []
                                        pulls_rqs_count = []
                                        for key, value in response.items():
                                            if key == 'url':
                                                pull_rs.append(key)
                                                pulls_rqs_count = len(pull_rs)
                                                pulls_json = {"repo_pulls_rqs_count": pulls_rqs_count}
                                else:
                                    pulls_rqs_count = 0
                                    pulls_json = {"repo_pulls_rqs_count": pulls_rqs_count}

                    print("---------------------")
                    print("Collecting community data")
                    community_json = {}
                    for urls in json_data.keys():
                        if urls == 'community':
                            community = json_data['community']
                            responses = requests.get(community)
                            response = responses.json()
                            if response is None or len(response) == 0:
                                health_percentage = ""
                                community_json = {"community_health_percentage": health_percentage}
                            else:
                                if 'health_percentage' in response:
                                    health_percentage = response['health_percentage']
                                    community_json = {"community_health_percentage": health_percentage}
                                else:
                                    health_percentage = ""
                                    community_json = {"community_health_percentage": health_percentage}

                    print("---------------------")
                    print("Collecting releases_url data")
                    releases_json = {}
                    for urls in json_data.keys():
                        if urls == 'releases_url':
                            releases_url = json_data['releases_url']
                            responses = requests.get(releases_url)
                            response = responses.json()
                            if response is None or len(response) == 0:
                                releases_url_name = ""
                                releases_count = 0
                                releases_url_published_at = ""
                                prerelease = ""
                                releases_json = {"releases_url_name": releases_url_name, "prerelease": prerelease,
                                                 "releases_count": releases_count,
                                                 "releases_url_published_at": releases_url_published_at,
                                                 }

                            else:
                                if response != {}:
                                    releases_count = 0
                                    if 'message' in response:
                                        releases_url_name = ""
                                        releases_count = 0
                                        releases_url_published_at = ""
                                        prerelease = ""
                                        releases_json = {"releases_url_name": releases_url_name,
                                                         "prerelease": prerelease,
                                                         "releases_count": releases_count,
                                                         "releases_url_published_at": releases_url_published_at,
                                                         }
                                    else:
                                        for release in response:
                                            releases_url_name = release['name']
                                            if release['url']:
                                                releases_count = releases_count + 1
                                                prerelease = release['prerelease']
                                                releases_url_published_at = release['published_at']
                                                releases_json = {"releases_url_name": releases_url_name,
                                                                 "prerelease": prerelease,
                                                                 "releases_count": releases_count,
                                                                 "releases_url_published_at": releases_url_published_at,
                                                                 }
                                            else:
                                                releases_url_name = ""
                                                releases_count = 0
                                                releases_url_published_at = ""
                                                prerelease = ""
                                                releases_json = {"releases_url_name": releases_url_name,
                                                                 "prerelease": prerelease,
                                                                 "releases_count": releases_count,
                                                                 "releases_url_published_at": releases_url_published_at,
                                                                 }

                    print("---------------------")
                    print("Collecting branch data")
                    branch_json = {}
                    for urls in json_data.keys():
                        if urls == 'branches_url':
                            branches = json_data['branches_url']
                            responses = requests.get(branches)
                            response = responses.json()
                            print("============branches_url_data============", response)
                            if response is None or len(response) == 0:
                                branch_name = ""
                                branches_count = 0
                                branch_json = {"branch_name": branch_name,
                                               "branches_count": branches_count}
                            else:
                                if response != {}:
                                    branches_count = 0
                                    if 'message' in response:
                                        branch_name = ""
                                        branches_count = 0
                                        branch_json = {"branch_name": branch_name,
                                                       "branches_count": branches_count}
                                    else:
                                        for branch in response:
                                            branch_name = branch['name']
                                            if branch['commit']['url']:
                                                branches_count = branches_count + 1
                                                branch_json = {"branch_name": branch_name,
                                                               "branches_count": branches_count}
                                            else:
                                                branches_count = 0
                                                branch_json = {"branch_name": branch_name,
                                                               "branches_count": branches_count}

                                else:
                                    branch_name = ""
                                    branches_count = 0
                                    branch_json = {"branch_name": branch_name,
                                                   "branches_count": branches_count}
                    print("---------------------")

                    print("Collecting language data")
                    language_json = {}
                    for urls in json_data.keys():
                        if urls == 'languages_url':
                            languages_url = json_data['languages_url']
                            responses = requests.get(languages_url)
                            response = responses.json()
                            if response != {}:
                                languages = []
                                language_count = []
                                for key, value in response.items():
                                    languages.append(key)
                                    language_count = len(languages)
                                    language_json = {"languages": languages, "languages_count": language_count}
                            else:
                                languages = ""
                                language_count = len(languages)
                                language_json = {"languages": languages, "languages_count": language_count}

                    print("---------------------")
                    print("Collecting repo pulls_url accepted and rejected  data")
                    repo_pulls_url_json = {}
                    for urls in json_data.keys():
                        if urls == 'pulls_url':
                            pulls_url = json_data['pulls_url']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============pulls_url============", response)

                            if response is None or len(response) == 0:
                                state_message = ""
                                pullrqs_accpted = 0
                                pullrqs_rejcted = 0
                                repo_pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                       "repo_pullrqs_rejcted": pullrqs_rejcted}
                            else:
                                if response != {}:
                                    pullrqs_accpted = 0
                                    pullrqs_rejcted = 0
                                    if 'message' in response:
                                        state_message = ""
                                        pullrqs_accpted = 0
                                        pullrqs_rejcted = 0
                                        repo_pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                               "repo_pullrqs_rejcted": pullrqs_rejcted}
                                    else:
                                        if 'state' in response:
                                            state_message = response['state']
                                            if state_message == "APPROVED":
                                                pullrqs_accpted = pullrqs_accpted + 1
                                            else:
                                                pullrqs_rejcted = pullrqs_rejcted + 1
                                                repo_pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                                       "repo_pullrqs_rejcted": pullrqs_rejcted}
                                        else:
                                            state_message = ""
                                            pullrqs_accpted = 0
                                            pullrqs_rejcted = 0
                                            repo_pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                                   "repo_pullrqs_rejcted": pullrqs_rejcted}
                                else:
                                    state_message = ""
                                    pullrqs_accpted = 0
                                    pullrqs_rejcted = 0
                                    repo_pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                           "repo_pullrqs_rejcted": pullrqs_rejcted}

                    print("---------------------")
                    print("Collecting user pulls_url accepted and rejected  data")
                    user_pulls_user_json = {}
                    for urls in json_data.keys():
                        if urls == 'pulls':
                            pulls_url = json_data['pulls']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============pulls============", response)

                            if response is None or len(response) == 0:
                                state_message = ""
                                pullrqs_accpted = 0
                                pullrqs_rejcted = 0
                                user_pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                        "user_pullrqs_rejcted": pullrqs_rejcted}
                            else:
                                if response != {}:
                                    pullrqs_accpted = 0
                                    pullrqs_rejcted = 0
                                    if 'message' in response:
                                        if 'state' in response:
                                            state_message = response['state']
                                            if state_message == "APPROVED":
                                                pullrqs_accpted = pullrqs_accpted + 1
                                            else:
                                                pullrqs_rejcted = pullrqs_rejcted + 1

                                            user_pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                                    "user_pullrqs_rejcted": pullrqs_rejcted}
                                        else:
                                            state_message = ""
                                            pullrqs_accpted = 0
                                            pullrqs_rejcted = 0
                                            user_pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                                    "user_pullrqs_rejcted": pullrqs_rejcted}
                                    else:
                                        state_message = ""
                                        pullrqs_accpted = 0
                                        pullrqs_rejcted = 0
                                        user_pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                                "user_pullrqs_rejcted": pullrqs_rejcted}
                                else:
                                    state_message = ""
                                    pullrqs_accpted = 0
                                    pullrqs_rejcted = 0
                                    user_pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                            "user_pullrqs_rejcted": pullrqs_rejcted}

                    print("---------------------")
                    print("Collecting repo pulls_url data")
                    repo_pullrqs_json = {}
                    for urls in json_data.keys():
                        if urls == 'repo_pulls_url':
                            pulls_url = json_data['repo_pulls_url']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============repo_pulls_url============", response)

                            if response is None or len(response) == 0:
                                count_repo_pullrqs = 0
                                repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}
                            else:
                                if response != {}:
                                    count_repo_pullrqs = 0
                                    if 'message' in response:
                                        count_repo_pullrqs = 0
                                        repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}
                                    else:
                                        for data in response:
                                            repo_pullrqs = data['url']
                                            if repo_pullrqs:
                                                count_repo_pullrqs = count_repo_pullrqs + 1
                                                repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}
                                            else:
                                                count_repo_pullrqs = 0
                                                repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}

                                else:
                                    count_repo_pullrqs = 0
                                    repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}

                    print("---------------------")
                    print("Collecting user pulls_url")
                    user_pullrqs_count_json = {}
                    for urls in json_data.keys():
                        if urls == 'user_pullrs':
                            pulls_url = json_data['user_pullrs']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============user_pullrs============", response)

                            if response is None or len(response) == 0:
                                count_user_pullrqs = 0
                                user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}
                            else:
                                if response != {}:
                                    count_user_pullrqs = 0
                                    if 'message' in response:
                                        count_user_pullrqs = 0
                                        user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}
                                    else:
                                        for data in response:
                                            repo_pullrqs = data['url']
                                            if repo_pullrqs:
                                                count_user_pullrqs = count_user_pullrqs + 1
                                                user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}
                                            else:
                                                count_user_pullrqs = 0
                                                user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}

                                else:
                                    count_user_pullrqs = 0
                                    user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}

                    print("---------------------")
                    print("Collecting branch pulls_url")
                    branch_pullrs_count_json = {}
                    for urls in json_data.keys():
                        if urls == 'user_pullrs':
                            pulls_url = json_data['user_pullrs']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============branch_pullrs============", response)

                            if response is None or len(response) == 0:
                                count_branch_pullrqs = 0
                                branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}
                            else:
                                if response != {}:
                                    heads = []
                                    if 'message' in response:
                                        count_branch_pullrqs = 0
                                        branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}
                                    else:
                                        for data in response:
                                            repo_pullrqs = data['url']
                                            heads_in_pullrqs = data['head']['ref']
                                            heads.append(heads_in_pullrqs)
                                            heads_count = len(heads)
                                            count_branch_pullrqs = heads_count + 1
                                            branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}


                                else:
                                    count_branch_pullrqs = 0
                                    branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}
                    print("---------------------")
                    print("Collecting branch_url data")
                    brnch_commit_json = {}
                    for urls in json_data.keys():
                        if urls == 'branch_url':
                            commits_url = json_data['branch_url']
                            responses = requests.get(commits_url)
                            response = responses.json()
                            print("============branch_url============", response)
                            if response is None or len(response) == 0:

                                commit_id = ""
                                commit_url = ""
                                count_commit_in_brnch = 0
                                brnch_commit_json = {"brnch_commit_id": commit_id,
                                                     "count_commit_in_brnch": count_commit_in_brnch}
                            else:
                                if response != {}:
                                    count_commit_in_brnch = 0
                                    if 'message' in response:
                                        count_commit_in_brnch = 0
                                        brnch_commit_json = {"brnch_commit_id": 0,
                                                             "count_commit_in_brnch": count_commit_in_brnch}
                                    else:
                                        for data in response:

                                            commit_id = data['commit']['sha']
                                            if data['commit']['url']:
                                                count_commit_in_brnch = count_commit_in_brnch + 1
                                                brnch_commit_json = {"brnch_commit_id": commit_id,
                                                                     "count_commit_in_brnch": count_commit_in_brnch}
                                            else:
                                                count_commit_in_brnch = 0
                                                brnch_commit_json = {"brnch_commit_id": commit_id,
                                                                     "count_commit_in_brnch": count_commit_in_brnch}
                                else:

                                    commit_id = ""
                                    commit_url = ""
                                    count_commit_in_brnch = 0
                                    brnch_commit_json = {"brnch_commit_id": commit_id,
                                                         "count_commit_in_brnch": count_commit_in_brnch}

                    repos_information = mergedict(json_data, language_json, branch_json, releases_json,
                                                  community_json, pulls_json, repo_json, branch_pullrs_count_json,
                                                  user_pullrqs_count_json, repo_pullrqs_json,
                                                  brnch_commit_json, repo_pulls_url_json, user_pulls_user_json)
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
                    branches_url = repos_information['branches_url']
                    branch_name = repos_information['branch_name']
                    branches_count = repos_information['branches_count']
                    brnch_commit_id = repos_information['brnch_commit_id']
                    branch_commit_count = repos_information['count_commit_in_brnch']
                    languages_url = repos_information['languages_url']
                    languages = repos_information['languages']
                    languages_count = repos_information['languages_count']
                    releases_url = repos_information['releases_url']
                    releases_url_name = repos_information['releases_url_name']
                    releases_count = repos_information['releases_count']
                    releases_url_published_at = repos_information['releases_url_published_at']
                    prerelease = repos_information['prerelease']
                    community_health_percentage = repos_information['community_health_percentage']
                    pulls_rqs_count = repos_information['repo_pulls_rqs_count']
                    count_user = repos_information['count_num_of_user']
                    repo_pullrqs_accpted = repos_information['repo_pullrqs_accpted']
                    repo_pullrqs_rejcted = repos_information['repo_pullrqs_rejcted']
                    user_pullrqs_accpted = repos_information['user_pullrqs_accpted']
                    user_pullrqs_rejcted = repos_information['user_pullrqs_rejcted']
                    count_repo_pullrqs = repos_information['count_repo_pullrqs']
                    count_user_pullrqs = repos_information['count_user_pullrqs']
                    count_branch_pullrqs = repos_information['count_branch_pullrqs']

                    json_datas = GitHub(repo_id, name, description, created_on, updated_on, owner, license,
                                        includes_wiki,
                                        forks_count, issues_count, stars_count, watchers_count, repo_url, commits_url,
                                        branches_url, branch_name, branches_count, brnch_commit_id, branch_commit_count,
                                        languages_url, languages, languages_count, releases_url, releases_url_name,
                                        releases_count, releases_url_published_at, prerelease,
                                        community_health_percentage, pulls_rqs_count, count_user,
                                        count_repo_pullrqs, count_user_pullrqs, count_branch_pullrqs,
                                        repo_pullrqs_accpted, repo_pullrqs_rejcted, user_pullrqs_accpted,
                                        user_pullrqs_rejcted)

                    # db.session.add(json_datas)
                    # db.session.commit()

            return make_response(jsonify({"msg": f"GitHub data successfully inserted."})), 201

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@gits.route('/api/getcommitgitdata', methods=['POST'])
def getcommitgitdata():
    try:
        if request.method == "POST":
            result = request.get_json(force=True)
            user_name = result['name']
            user_password = result['password']
            projectid = result['projectid']
            git_url = result['url']
            data = ToolsLogin.query.filter(ToolsLogin.name == user_name, ToolsLogin.projectid == projectid)
            if user_name and check_password_hash(data.first().password, user_password):
                data = requests.get(git_url + user_name)
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
                    data.append({"default_branch": repo['default_branch']})
                    data.append({"repo_url": repo['url']})
                    data.append({"commits_url": repo['commits_url'].split("{")[0]})
                    for i in data:
                        json_data.update(i)
                    print("---------------------")
                    print("Collecting repo commit data")
                    commit_json = {}
                    for urls in json_data.keys():
                        if urls == 'commits_url':
                            commits_url = json_data['commits_url']
                            responses = requests.get(commits_url)
                            response = responses.json()
                            print("============commits_url============", response)
                            #
                            if response is None or len(response) == 0:
                                commit_id = ""
                                commit_date = ""
                                commit_msg = ""
                                commit_json = {"commit_id": commit_id, "commit_date": commit_date,
                                               "commit_msg": commit_msg}
                            else:
                                if response != {}:
                                    for commit in response:
                                        commit_id = commit['sha']
                                        commit_date = commit['commit']['committer']['date']
                                        commit_msg = commit['commit']['message']
                                        commit_json = {"commit_id": commit_id, "commit_date": commit_date,
                                                       "commit_msg": commit_msg}

                                else:
                                    commit_id = ""
                                    commit_date = ""
                                    commit_msg = ""
                                    commit_json = {"commit_id": commit_id, "commit_date": commit_date,
                                                   "commit_msg": commit_msg}

                    repos_information = mergedict(json_data, commit_json)
                    print("repos_information", repos_information)

                    repo_id = repos_information['repo_id']
                    commit_id = repos_information['commit_id']
                    commit_date = repos_information['commit_date']
                    commit_msg = repos_information['commit_msg']

                    json_datas = GitCommitInfo(repo_id, commit_id, commit_date, commit_msg)

                    db.session.add(json_datas)
                    db.session.commit()

        return make_response(jsonify({"msg": f"GitHub collect repo commit data successfully inserted."})), 201
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@gits.route('/api/getbranchcommitdata', methods=['POST'])
def getbranchcommitdata():
    try:
        if request.method == "POST":
            result = request.get_json(force=True)
            user_name = result['name']
            user_password = result['password']
            projectid = result['projectid']
            git_url = result['url']
            data = ToolsLogin.query.filter(ToolsLogin.name == user_name, ToolsLogin.projectid == projectid)
            if user_name and check_password_hash(data.first().password, user_password):
                data = requests.get(git_url + user_name)
                datas = data.json()
                # print("------------datas---------", datas)

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
                    data.append({"default_branch": repo['default_branch']})
                    data.append({"user_url": repo['url']})
                    data.append({"branch_url": repo['url'] + '/branches'})
                    data.append({"commits_url": repo['commits_url'].split("{")[0]})

                    for i in data:
                        json_data.update(i)
                    print("---------------------")
                    print("Collecting branch_url data")
                    brnch_commit_json = {}
                    for urls in json_data.keys():
                        if urls == 'branch_url':
                            commits_url = json_data['branch_url']
                            responses = requests.get(commits_url)
                            response = responses.json()
                            print("============branch_url============", response)
                            if response is None or len(response) == 0:
                                branch_name = ""
                                commit_id = ""
                                commit_url = ""
                                count_commit_in_brnch = 0
                                brnch_commit_json = {"branch_name": branch_name, "commit_id": commit_id,
                                                     "count_commit_in_brnch": count_commit_in_brnch}
                            else:
                                if response != {}:
                                    count_commit_in_brnch = 0
                                    for data in response:
                                        branch_name = data['name']
                                        commit_id = data['commit']['sha']
                                        commit_url = data['commit']['url']
                                        if data['commit']['url'] == commit_url:
                                            count_commit_in_brnch = count_commit_in_brnch + 1
                                            brnch_commit_json = {"branch_name": branch_name, "commit_id": commit_id,
                                                                 "count_commit_in_brnch": count_commit_in_brnch}
                                        else:
                                            count_commit_in_brnch = 0
                                            brnch_commit_json = {"branch_name": branch_name, "commit_id": commit_id,
                                                                 "count_commit_in_brnch": count_commit_in_brnch}

                                else:
                                    branch_name = ""
                                    commit_id = ""
                                    commit_url = ""
                                    count_commit_in_brnch = 0
                                    brnch_commit_json = {"branch_name": branch_name, "commit_id": commit_id,
                                                         "count_commit_in_brnch": count_commit_in_brnch}

                    repos_information = mergedict(json_data, brnch_commit_json)
                    print("repos_information", repos_information)

                    repo_id = repos_information['repo_id']
                    branch_name = repos_information['branch_name']
                    commit_id = repos_information['commit_id']
                    count_commit_in_brnch = repos_information['count_commit_in_brnch']

                    json_datas = GitCommitInfo(repo_id, branch_name, commit_id, count_commit_in_brnch)

                    # db.session.add(json_datas)
                    # db.session.commit()

        return make_response(jsonify({"msg": f"GitHub collect branch commit data successfully inserted."})), 201
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@gits.route('/api/getuserpullrqsdata', methods=['POST'])
def getuserpullrqsdata():
    try:
        if request.method == "POST":
            result = request.get_json(force=True)
            user_name = result['name']
            user_password = result['password']
            projectid = result['projectid']
            git_url = result['url']
            data = ToolsLogin.query.filter(ToolsLogin.name == user_name, ToolsLogin.projectid == projectid)
            if user_name and check_password_hash(data.first().password, user_password):
                data = requests.get(git_url + user_name)
                datas = data.json()
                # print("------------datas---------", datas)

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

                for i, repo in enumerate(repos_data):
                    data = []
                    json_data = {}
                    data.append({"repo_id": repo['id']})
                    data.append({"name": repo['name']})
                    data.append({"default_branch": repo['default_branch']})
                    data.append({"user_url": repo['url']})
                    data.append({"branch_url": repo['url'] + '/branches'})
                    # data.append({"pulls_url": repo['url'] + '/pulls/{pull_number}/merge'})
                    data.append({"commits_url": repo['commits_url'].split("{")[0]})
                    data.append({"pulls_url": repo['pulls_url'].split("{")[0] + '/reviews'})
                    data.append({"repo_pulls_url": repo['pulls_url'].split("{")[0]})
                    data.append({"pulls": repo['url'] + '/pulls'})
                    data.append({"user_pullrs": repo['url'] + '/pulls'})

                    for i in data:
                        json_data.update(i)
                    print("---------------------")
                    print("Collecting pulls in user data")

                    pullrqs_url_json = {}
                    for urls in json_data.keys():
                        if urls == 'pulls':
                            pulls = json_data['pulls']
                            responses = requests.get(pulls)
                            response = responses.json()
                            print("============pulls_url============", response)
                            if response is None or len(response) == 0:
                                pullrs_in_user = 0
                                pullrqs_url_json = {"pullrs_in_user": pullrs_in_user}
                            else:
                                if response != {}:
                                    pullrs_in_user = 0
                                    for data in response:
                                        pull_url = data['url']
                                        pullrs_date = data['pushed_at']
                                        pullrs_date = data['created_at']
                                        pullrs_date = data['updated_at']
                                        pull_type = data['user']['type']
                                        if pull_type == 'User':
                                            pullrs_in_user = pullrs_in_user + 1
                                            pullrqs_url_json = {"pullrs_in_user": pullrs_in_user}

                                        else:
                                            pullrs_in_user = 0
                                            pullrqs_url_json = {"pullrs_in_user": pullrs_in_user}

                    print("---------------------")
                    print("Collecting repo pulls_url accepted and rejected  data")
                    pulls_url_json = {}
                    for urls in json_data.keys():
                        if urls == 'pulls_url':
                            pulls_url = json_data['pulls_url']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============pulls_url============", response)

                            if response is None or len(response) == 0:
                                state_message = ""
                                pullrqs_accpted = 0
                                pullrqs_rejcted = 0
                                pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                  "repo_pullrqs_rejcted": pullrqs_rejcted}
                            else:
                                pullrqs_accpted = 0
                                pullrqs_rejcted = 0
                                if 'state' in response:
                                    state_message = response['state']
                                    if state_message == "APPROVED":
                                        pullrqs_accpted = pullrqs_accpted + 1
                                    else:
                                        pullrqs_rejcted = pullrqs_rejcted + 1

                                    pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                      "repo_pullrqs_rejcted": pullrqs_rejcted}

                                else:
                                    state_message = ""
                                    pullrqs_accpted = 0
                                    pullrqs_rejcted = 0
                                    pulls_url_json = {"repo_pullrqs_accpted": pullrqs_accpted,
                                                      "repo_pullrqs_rejcted": pullrqs_rejcted}

                    print("---------------------")
                    print("Collecting user pulls_url accepted and rejected  data")
                    pulls_user_json = {}
                    for urls in json_data.keys():
                        if urls == 'pulls':
                            pulls_url = json_data['pulls']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============pulls============", response)

                            if response is None or len(response) == 0:
                                state_message = ""
                                pullrqs_accpted = 0
                                pullrqs_rejcted = 0
                                pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                   "user_pullrqs_rejcted": pullrqs_rejcted}
                            else:
                                pullrqs_accpted = 0
                                pullrqs_rejcted = 0
                                if 'state' in response:
                                    state_message = response['state']
                                    if state_message == "APPROVED":
                                        pullrqs_accpted = pullrqs_accpted + 1
                                    else:
                                        pullrqs_rejcted = pullrqs_rejcted + 1

                                    pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                       "user_pullrqs_rejcted": pullrqs_rejcted}

                                else:
                                    state_message = ""
                                    pullrqs_accpted = 0
                                    pullrqs_rejcted = 0
                                    pulls_user_json = {"user_pullrqs_accpted": pullrqs_accpted,
                                                       "user_pullrqs_rejcted": pullrqs_rejcted}

                    print("---------------------")
                    print("Collecting repo pulls_url data")
                    repo_pullrqs_json = {}
                    for urls in json_data.keys():
                        if urls == 'repo_pulls_url':
                            pulls_url = json_data['repo_pulls_url']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============repo_pulls_url============", response)

                            if response is None or len(response) == 0:
                                count_repo_pullrqs = 0
                                repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}
                            else:
                                if response != {}:
                                    count_repo_pullrqs = 0
                                    for data in response:
                                        repo_pullrqs = data['url']
                                        if repo_pullrqs:
                                            count_repo_pullrqs = count_repo_pullrqs + 1
                                            repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}
                                        else:
                                            count_repo_pullrqs = 0
                                            repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}

                                else:
                                    count_repo_pullrqs = 0
                                    repo_pullrqs_json = {"count_repo_pullrqs": count_repo_pullrqs}

                    print("---------------------")
                    print("Collecting user pulls_url")
                    user_pullrqs_count_json = {}
                    for urls in json_data.keys():
                        if urls == 'user_pullrs':
                            pulls_url = json_data['user_pullrs']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============user_pullrs============", response)

                            if response is None or len(response) == 0:
                                count_user_pullrqs = 0
                                user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}
                            else:
                                if response != {}:
                                    count_user_pullrqs = 0
                                    for data in response:
                                        repo_pullrqs = data['url']
                                        if repo_pullrqs:
                                            count_user_pullrqs = count_user_pullrqs + 1
                                            user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}
                                        else:
                                            count_user_pullrqs = 0
                                            user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}

                                else:
                                    count_user_pullrqs = 0
                                    user_pullrqs_count_json = {"count_user_pullrqs": count_user_pullrqs}

                    print("---------------------")
                    print("Collecting branch pulls_url")
                    branch_pullrs_count_json = {}
                    for urls in json_data.keys():
                        if urls == 'user_pullrs':
                            pulls_url = json_data['user_pullrs']
                            responses = requests.get(pulls_url)
                            response = responses.json()
                            print("============branch_pullrs============", response)

                            if response is None or len(response) == 0:
                                count_branch_pullrqs = 0
                                branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}
                            else:
                                if response != {}:
                                    heads = []
                                    for data in response:
                                        repo_pullrqs = data['url']
                                        heads_in_pullrqs = data['head']['ref']
                                        heads.append(heads_in_pullrqs)
                                        heads_count = len(heads)
                                        count_branch_pullrqs = heads_count + 1
                                        branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}
                                else:
                                    count_branch_pullrqs = 0
                                    branch_pullrs_count_json = {"count_branch_pullrqs": count_branch_pullrqs}

                    repos_information = mergedict(json_data, pulls_url_json, pullrqs_url_json, pulls_user_json,
                                                  repo_pullrqs_json, user_pullrqs_count_json, branch_pullrs_count_json)
                    print("repos_information", repos_information)
                    #
                    repo_id = repos_information['repo_id']
                    pullrs_in_user = repos_information['pullrs_in_user']
                    repo_pullrqs_accpted = repos_information['repo_pullrqs_accpted']
                    repo_pullrqs_rejcted = repos_information['repo_pullrqs_rejcted']
                    user_pullrqs_accpted = repos_information['user_pullrqs_accpted']
                    user_pullrqs_rejcted = repos_information['user_pullrqs_rejcted']
                    count_repo_pullrqs = repos_information['count_repo_pullrqs']
                    count_user_pullrqs = repos_information['count_user_pullrqs']
                    count_branch_pullrqs = repos_information['count_branch_pullrqs']

                    #
                    # json_datas = GitCommitInfo(repo_id, pullrs_in_user,repo_pullrqs_accpted, repo_pullrqs_rejcted)

                    # db.session.add(json_datas)
                    # db.session.commit()

        return make_response(jsonify({"msg": f"GitHub collect user and repo pullrqs data successfully inserted."})), 201
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
