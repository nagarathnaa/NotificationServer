import gitlab


class DevOpsGitlab:

    # def __init__(self, url, http_username, http_password):
    def __init__(self, url, private_token, api_version=4):
        # self.gitlab_server = gitlab.Gitlab(url, http_username, http_password)
        self.gitlab_server = gitlab.Gitlab(url, private_token, api_version=4)

        author = self.gitlab_server

        version = self.gitlab_server._api_version
        print("GitLab Version: {}".format(version))
        user = self.gitlab_server.http_username
        # for name in user:
        print("GitLab User: {}".format(user))

    def get_gitlab_project(self):
        projects_name = []
        projects_id = []
        projects = self.gitlab_server.projects.list()
        count_projects = 0
        for project in projects:
            # print("==============", project.attributes)
            projects_name.append(project.attributes['name'])
            projects_id.append(project.attributes['id'])
            count_projects = len(projects_id)

        return {"projects_id": projects_id, "projects_name": projects_name, 'count_projects': count_projects}

    def get_gitlab_users(self):
        users_name = []
        userss = self.gitlab_server.users.list()
        for user in userss:
            # print("==============", user.attributes)
            users_name.append(user.attributes['username'])

        return {"users_name": users_name}

    #
    def get_gitlab_namespaces(self):
        namespaces_name = []
        namespaces = self.gitlab_server.namespaces.list()
        for names in namespaces:
            # print("==============", names.attributes)
            namespaces_name.append(names.attributes['name'])

        return {"namespaces_name": namespaces_name}

    def get_gitlab_broadcastmessages(self):
        messages = []
        broadcastmessages = self.gitlab_server.broadcastmessages.list()
        for message in broadcastmessages:
            # print("=====broadcastmessages=========", message.attributes)
            messages.append(message.attributes['message'])
        return {"broadcastmessages": messages}

    def get_gitlab_groups(self):
        groups_list = []
        groups = self.gitlab_server.groups.list()
        count_groups_list = 0
        for gp in groups:
            # print("=====deploykeys=========", gp.attributes)
            groups_list.append(gp.attributes['name'])
            count_groups_list = len(groups_list)
        return {"groups_list": groups_list, 'count_groups_list': count_groups_list}

    def get_gitlab_issues(self):
        issues_list = []
        issues = self.gitlab_server.issues.list()
        count_issues_list = 0
        for iss in issues:
            # print("=====deploykeys=========", iss.attributes)
            issues_list.append(iss.attributes['name'])
            count_issues_list = len(issues_list)
        return {"issues_list": issues_list, 'count_issues_list': count_issues_list}

    def get_gitlab_licenses(self):
        licenses_list = []
        licenses = self.gitlab_server.licenses.list()
        for iss in licenses:
            # print("=====licenses=========", iss.attributes)
            licenses_list.append(iss.attributes['key'])
        return {"licenses_list": licenses_list}

    def get_gitlab_mergerequests(self):
        mergerequests_list = []
        mergerequests = self.gitlab_server.mergerequests.list()
        for mrg in mergerequests:
            print("=====mergerequests_list=========", mrg.attributes)
            # mergerequests_list.append(mrg.attributes['key'])
        return {"mergerequests_list": mergerequests_list}

    def get_gitlab_dockerfiles(self):
        dockerfiles_list = []
        dockerfiles = self.gitlab_server.dockerfiles.list()
        count_dockerfiles_list = 0
        for files in dockerfiles:
            # print("=====dockerfiles=========", files.attributes)
            dockerfiles_list.append(files.attributes['key'])
            count_dockerfiles_list = len(dockerfiles_list)
        return {"dockerfiles_list": dockerfiles_list, 'count_dockerfiles_list': count_dockerfiles_list}

    def get_gitlab_gitlabciymls(self):
        gitlabciymls_list = []
        gitlabciymls = self.gitlab_server.gitlabciymls.list()
        count_gitlabciymls_list = 0
        for ymls in gitlabciymls:
            # print("=====variables=========", ymls.attributes)
            gitlabciymls_list.append(ymls.attributes['key'])
            count_gitlabciymls_list = len(gitlabciymls_list)
        return {"gitlabciymls_list": gitlabciymls_list, 'count_gitlabciymls_list': count_gitlabciymls_list}

    def get_gitlab_snippets(self):
        gitlab_snippets_list = []
        snippets = self.gitlab_server.snippets.list()
        count_snippets = 0
        for snpt in snippets:
            # print("=====snippets=========", snpt.attributes)
            gitlab_snippets_list.append(snpt.attributes['key'])
            count_snippets = len(gitlab_snippets_list)
        return {"gitlab_snippets_list": gitlab_snippets_list, "count_snippets_list": count_snippets}

    def get_gitlab_events(self):
        gitlab_events_lists = []
        events_created_at = []
        events_lists = self.gitlab_server.events.list()
        count_events = 0
        for events in events_lists:
            # print("=====events_lists=========", events.attributes)
            events_created_at.append(events.attributes['created_at'])
            gitlab_events_lists.append(events.attributes['id'])
            count_events = len(gitlab_events_lists)

        return {"gitlab_events_lists": gitlab_events_lists,
                "count_events_list": count_events, "events_created_at": events_created_at}

    def get_gitlab_events_commits_and_date(self):
        events_commits_count = []
        events_lists = self.gitlab_server.events.list()
        count_events_commits = 0
        for events in events_lists:
            # print("=====events_lists_commit=========", events.attributes)
            if events.attributes['push_data'] != None:
                events_commits_count.append(events.attributes['push_data']['commit_count'])
                count_events_commits = len(events_commits_count)
            else:
                count_events_commits = 0
            return {"count_events_commits": count_events_commits}


if __name__ == '__main__':
    # gl = DevOpsGitlab('https://gitlab.com/', 'smruti_biswal', '@@mummy@@900@@')
    gl = DevOpsGitlab('https://gitlab.com', 'Z1ChLeFHEGgE7abSp2tY')
    projects_name = gl.get_gitlab_project()
    print("projects_name", projects_name)

    # project_branch = gl.get_gitlab_project_branch()
    # print("project_branch", project_branch)

    users_name = gl.get_gitlab_users()
    print("users_name", users_name)

    namespaces_name = gl.get_gitlab_namespaces()
    print("namespaces_name", namespaces_name)

    broadcastmessages = gl.get_gitlab_broadcastmessages()
    print("broadcastmessages", broadcastmessages)

    groups = gl.get_gitlab_groups()
    print("groups", groups)

    issues = gl.get_gitlab_issues()
    print("issues", issues)

    licenses = gl.get_gitlab_licenses()
    print("licenses", licenses)

    mergerequests = gl.get_gitlab_mergerequests()
    print("mergerequests", mergerequests)

    dockerfiles = gl.get_gitlab_dockerfiles()
    print("dockerfiles", dockerfiles)

    gitlabciymls_list = gl.get_gitlab_gitlabciymls()
    print("gitlabciymls_list", gitlabciymls_list)

    gitlab_snippets = gl.get_gitlab_snippets()
    print("gitlab_snippets_list", gitlab_snippets)

    gitlab_events = gl.get_gitlab_events()
    print("gitlab_events_lists", gitlab_events)
    get_gitlab_events_commits_and_date = gl.get_gitlab_events_commits_and_date()
    print("get_gitlab_events_commits_and_date", get_gitlab_events_commits_and_date)
