from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.tools_jenkins_model import Tools
from DOEAssessmentApp.DOE_models.tools_login_model import ToolsLogin
# from DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.jenkins_server import DevOpsJenkins
from werkzeug.security import generate_password_hash, check_password_hash

tools = Blueprint('tools', __name__)

colstools = ['id', 'job_name', 'total_no_build', 'total_no_success', 'total_no_failure', 'lastBuild_number',
             'lastBuild_duration', 'lastBuild_user', 'lastBuild_result', 'lastCompletedBuild_number',
             'lastCompletedBuild_duration', 'lastCompletedBuild_user', 'lastFailedBuild_number',
             'lastFailedBuild_duration',
             'lastFailedBuild_user', 'lastStableBuild_number', 'lastStableBuild_duration', 'lastSuccessfulBuild_number',
             'lastSuccessfulBuild_duration', 'lastUnstableBuild', 'healthReport_score', 'lastUnsuccessfulBuild_number',
             'lastUnsuccessfulBuild_duration', 'lastUnsuccessfulBuild_user', 'lastSuccessfulBuild_user',
             'lastStableBuild_user', 'creationdatetime', 'updationdatetime']


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@tools.route('/api/getjenkinsdata', methods=['GET'])
def getjenkinsdata():
    try:
        if request.method == "GET":
            data = Tools.query.all()
            result = [{col: getattr(d, col) for col in colstools} for d in data]
            return jsonify({"data": result}), 200
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@tools.route('/api/storejenkinsdata', methods=['POST'])
def storejenkinsdata():
    try:
        if request.method == "POST":
            result = request.get_json(force=True)
            user_name = result['name']
            user_password = result['password']
            projectid = result['projectid']
            data = ToolsLogin.query.filter(ToolsLogin.name == user_name,ToolsLogin.projectid == projectid)
            if user_name and check_password_hash(data.first().password, user_password):
                dev = DevOpsJenkins(result['url'], result['name'], result['password'])
                job_names = dev.alljobs()
                print(job_names)
                results = []
                for ele in job_names.keys():
                    result1 = job_names[ele]
                    for ele in range(len(result1)):
                        result = result1[ele]
                        results.append(result)
                for job in results:
                    jobs = dev.jenkins_server.get_job_info(job)
                    if '_class' in jobs.keys():
                        if jobs["_class"] == 'com.cloudbees.hudson.plugins.folder.Folder':
                            results.remove(job)

                for item in results:
                    failure_success_count = dev.failure_success_count(item)
                    print("===============", failure_success_count)
                    total_number_of_build = dev.total_number_of_build(item)
                    print("=======================", total_number_of_build)
                    count_details_build_info = dev.count_details_build_info(item)
                    print("=====================================", count_details_build_info)
                    json_data = mergedict({'job_name': item}, total_number_of_build, failure_success_count,
                                          count_details_build_info)
                    job_name = json_data['job_name']
                    total_no_build = json_data['total_no_build']
                    total_no_success = json_data['total_no_success']
                    total_no_failure = json_data['total_no_failure']
                    lastBuild_number = json_data['lastBuild_number']
                    lastBuild_duration = json_data['lastBuild_duration']
                    lastBuild_user = json_data['lastBuild_user']
                    lastBuild_result = json_data['lastBuild_result']
                    lastCompletedBuild_number = json_data['lastCompletedBuild_number']
                    lastCompletedBuild_duration = json_data['lastCompletedBuild_duration']
                    lastCompletedBuild_user = json_data['lastCompletedBuild_user']
                    lastFailedBuild_number = json_data['lastFailedBuild_number']
                    lastFailedBuild_duration = json_data['lastFailedBuild_duration']
                    lastFailedBuild_user = json_data['lastFailedBuild_user']
                    lastStableBuild_number = json_data['lastStableBuild_number']
                    lastStableBuild_duration = json_data['lastStableBuild_duration']
                    lastSuccessfulBuild_number = json_data['lastSuccessfulBuild_number']
                    lastSuccessfulBuild_duration = json_data['lastSuccessfulBuild_duration']
                    lastUnstableBuild = json_data['lastUnstableBuild']
                    healthReport_score = json_data['healthReport_score']
                    lastUnsuccessfulBuild_number = json_data['lastUnsuccessfulBuild_number']
                    lastUnsuccessfulBuild_duration = json_data['lastUnsuccessfulBuild_duration']
                    lastUnsuccessfulBuild_user = json_data['lastUnsuccessfulBuild_user']
                    lastSuccessfulBuild_user = json_data['lastSuccessfulBuild_user']
                    lastStableBuild_user = json_data['lastStableBuild_user']
                    json_datas = Tools(job_name, total_no_build, total_no_success, total_no_failure, lastBuild_number,
                                       lastBuild_duration, lastBuild_user, lastBuild_result, lastCompletedBuild_number,
                                       lastCompletedBuild_duration, lastCompletedBuild_user, lastFailedBuild_number,
                                       lastFailedBuild_duration, lastFailedBuild_user, lastStableBuild_number,
                                       lastStableBuild_duration, lastSuccessfulBuild_number,
                                       lastSuccessfulBuild_duration, lastUnstableBuild, healthReport_score,
                                       lastUnsuccessfulBuild_number, lastUnsuccessfulBuild_duration,
                                       lastUnsuccessfulBuild_user, lastSuccessfulBuild_user, lastStableBuild_user)
                    db.session.add(json_datas)
                    db.session.commit()
                return make_response(jsonify({"msg": f"Jenkinsdata successfully inserted."})), 201
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500

# @tools.route('/api/showdatasingraph', methods=['GET'])
# def showdatasingraph():
#     try:
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             auth_token = auth_header.split(" ")[1]
#         else:
#             auth_token = ''
#         if auth_token:
#             resp = Companyuserdetails.decode_auth_token(auth_token)
#             if isinstance(resp, str):
#                 if request.method == "GET":
#                     # data = Tools.query.all()


# class ShowDatasinGraph(Resource):
#     @classmethod
#     def get(self, job_name):
#         result = toolsetting_services.get_jenkins_job_status(job_name, message_bus.uow)
#
#         if not result:
#             return jsonify({'response': 'failure', 'msg': 'Candidate not found'}), 404
#         return {'response': 'success', 'results': result}, 200
