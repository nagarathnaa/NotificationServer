import jenkins

class DevOpsJenkins:
    buildDurations = []
    buildtimestamps = []
    totalDuration = 0.0

    def __init__(self, url, user, password):

        self.jenkins_server = jenkins.Jenkins(url, user, password)
        user = self.jenkins_server.get_whoami()
        version = self.jenkins_server.get_version()
        print("Jenkins Version: {}".format(version))
        print("Jenkins User: {}".format(user['id']))

    def alljobs(self):

        list_jobs = []
        jobs = self.jenkins_server.get_all_jobs()

        for x in jobs:
            list_jobs.append(x["fullname"])
        return {"name": list_jobs}

    def failure_success_count(self, name):
        jobs_info = self.jenkins_server.get_job_info(name)
        build_info = jobs_info["builds"]
        total_no_success = 0
        total_no_failure = 0
        for ele in build_info:
            if 'number' in ele.keys():
                builds_info = self.jenkins_server.get_build_info(name, ele['number'])
                result_success = builds_info['result']
                if result_success == "SUCCESS":
                    total_no_success = total_no_success + 1
                if result_success == "FAILURE":
                    total_no_failure = total_no_failure + 1

        return {"total_no_success": total_no_success, "total_no_failure": total_no_failure}

    def total_number_of_build(self, name):
        jobs_info = self.jenkins_server.get_job_info(name)
        build_info = jobs_info["builds"]
        count = 0
        for ele in build_info:
            if 'number' in ele.keys():
                count += 1

        return {"total_no_build": count}

    def read_user_name(self, args):
        result = ''
        for arg in args:
            if 'causes' in arg.keys():
                if arg["causes"][0]["_class"] == "hudson.model.Cause$UserIdCause":
                    res1 = arg["causes"][0]["userName"]
                if arg["causes"][0]["_class"] == "hudson.model.Cause$RemoteCause":
                    res1 = arg["causes"][0]["addr"]
        return result

    def count_details_build_info(self, name):
        jobs = self.jenkins_server.get_job_info(name)
        lastUnstableBuild = jobs["lastUnstableBuild"]
        if jobs["healthReport"] is None or len(jobs["healthReport"]) == 0:
            healthReport_score = 0
        else:
            healthReport = jobs["healthReport"][0]
            if 'score' in healthReport:
                healthReport_score = healthReport['score']
            else:
                healthReport_score = 0

        if jobs["lastBuild"] is None:
            lastBuild_number = 0
        else:

            lastBuild = jobs["lastBuild"]
            lastBuild_number = lastBuild.get('number')
        if lastBuild_number != 0:
            lastBuild_number_durations = self.jenkins_server.get_build_info(name, lastBuild_number)
            lastBuild_duration = lastBuild_number_durations["duration"]
            lastBuild_result = lastBuild_number_durations["result"]
            lastBuild_users = lastBuild_number_durations["actions"]
            lastBuild_user = self.read_user_name(lastBuild_users)
        else:
            lastBuild_duration = ''
            lastBuild_user = ''
            lastBuild_result = ''

        if jobs["lastCompletedBuild"] is None:
            lastCompletedBuild_number = 0
        else:

            lastCompletedBuild = jobs["lastCompletedBuild"]
            lastCompletedBuild_number = lastCompletedBuild.get('number')
        if lastCompletedBuild_number != 0:
            lastCompletedBuild_number_durations = self.jenkins_server.get_build_info(name, lastCompletedBuild_number)
            lastCompletedBuild_duration = lastCompletedBuild_number_durations["duration"]
            lastCompletedBuild_users = lastCompletedBuild_number_durations["actions"]
            lastCompletedBuild_user = self.read_user_name(lastCompletedBuild_users)
        else:
            lastCompletedBuild_duration = ''
            lastCompletedBuild_user = ''

        if jobs["lastFailedBuild"] is None:
            lastFailedBuild_number = 0
        else:
            lastFailedBuild = jobs["lastFailedBuild"]
            lastFailedBuild_number = lastFailedBuild.get('number')
        if lastFailedBuild_number != 0:
            lastFailedBuild_number_durations = self.jenkins_server.get_build_info(name, lastFailedBuild_number)
            lastFailedBuild_duration = lastFailedBuild_number_durations["duration"]
            lastFailedBuild_users = lastFailedBuild_number_durations["actions"]
            lastFailedBuild_user = self.read_user_name(lastFailedBuild_users)
        else:
            lastFailedBuild_duration = ''
            lastFailedBuild_user = ''

        if jobs["lastStableBuild"] is None:

            lastStableBuild_number = 0
        else:

            lastStableBuild = jobs["lastStableBuild"]
            lastStableBuild_number = lastStableBuild.get('number')

        if lastStableBuild_number != 0:

            lastStableBuild_number_durations = self.jenkins_server.get_build_info(name, lastStableBuild_number)
            lastStableBuild_duration = lastStableBuild_number_durations["duration"]
            lastStableBuild_number_users = lastStableBuild_number_durations["actions"]
            lastStableBuild_user = self.read_user_name(lastStableBuild_number_users)
        else:
            lastStableBuild_duration = ''
            lastStableBuild_user = ''

        if jobs["lastSuccessfulBuild"] is None:

            lastSuccessfulBuild_number = 0
        else:

            lastSuccessfulBuild = jobs["lastSuccessfulBuild"]
            lastSuccessfulBuild_number = lastSuccessfulBuild.get('number')
        if lastSuccessfulBuild_number != 0:

            lastSuccessfulBuild_number_durations = self.jenkins_server.get_build_info(name, lastSuccessfulBuild_number)
            lastSuccessfulBuild_duration = lastSuccessfulBuild_number_durations["duration"]
            lastSuccessfulBuild_number_users = lastSuccessfulBuild_number_durations["actions"]
            lastSuccessfulBuild_user = self.read_user_name(lastSuccessfulBuild_number_users)
        else:
            lastSuccessfulBuild_duration = ''
            lastSuccessfulBuild_user = ''

        if jobs["lastUnsuccessfulBuild"] is None:

            lastUnsuccessfulBuild_number = 0
        else:

            lastUnsuccessfulBuild = jobs["lastUnsuccessfulBuild"]
            lastUnsuccessfulBuild_number = lastUnsuccessfulBuild.get('number')
        if lastUnsuccessfulBuild_number != 0:
            lastUnsuccessfulBuild_number_durations = self.jenkins_server.get_build_info(name,
                                                                                        lastUnsuccessfulBuild_number)
            lastUnsuccessfulBuild_duration = lastUnsuccessfulBuild_number_durations["duration"]
            lastUnsuccessfulBuild_users = lastUnsuccessfulBuild_number_durations["actions"]
            lastUnsuccessfulBuild_user = self.read_user_name(lastUnsuccessfulBuild_users)
        else:
            lastUnsuccessfulBuild_duration = ''
            lastUnsuccessfulBuild_user = ''

        return {"lastBuild_number": lastBuild_number,
                "lastBuild_duration": lastBuild_duration,
                "lastBuild_user": lastBuild_user,
                "lastBuild_result": lastBuild_result,
                "lastCompletedBuild_number": lastCompletedBuild_number,
                "lastCompletedBuild_duration": lastCompletedBuild_duration,
                "lastCompletedBuild_user": lastCompletedBuild_user,
                "lastFailedBuild_number": lastFailedBuild_number,
                "lastFailedBuild_duration": lastFailedBuild_duration,
                "lastFailedBuild_user": lastFailedBuild_user,
                "lastStableBuild_number": lastStableBuild_number,
                "lastStableBuild_duration": lastStableBuild_duration,
                "lastSuccessfulBuild_number": lastSuccessfulBuild_number,
                "lastSuccessfulBuild_duration": lastSuccessfulBuild_duration,
                "lastUnstableBuild": lastUnstableBuild,
                "healthReport_score": healthReport_score,
                "lastUnsuccessfulBuild_number": lastUnsuccessfulBuild_number,
                "lastUnsuccessfulBuild_duration": lastUnsuccessfulBuild_duration,
                "lastUnsuccessfulBuild_user": lastUnsuccessfulBuild_user,
                "lastSuccessfulBuild_user": lastSuccessfulBuild_user,
                "lastStableBuild_user": lastStableBuild_user}

