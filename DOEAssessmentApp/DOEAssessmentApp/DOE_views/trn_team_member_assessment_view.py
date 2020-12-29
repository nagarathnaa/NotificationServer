from datetime import datetime
from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.trn_team_member_assessment_model import QuestionsAnswered
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.question_model import Question

assessment = Blueprint('assessment', __name__)


@assessment.route('/api/submitassessment', methods=['PUT'])
def submitassessment():
    try:
        totalscoreachieved = 0
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
                if request.method == "PUT":
                    res = request.get_json(force=True)
                    if 'assessment_id' in res:
                        assessmentid = res['assessment_id']
                    else:
                        empid = res['emp_id']
                        projid = res['projectid']
                        areaid = res['area_id']
                        funcid = res['functionality_id']
                        if "subfunc_id" in res:
                            subfuncid = res['subfunc_id']
                            combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                        else:
                            combination = str(empid) + str(projid) + str(areaid) + str(funcid)
                        existing_assessment = Assessment.query.filter_by(combination=combination).first()
                        assessmentid = existing_assessment.id
                    data_proj = Project.query.filter_by(id=projid).first()
                    if data_proj.needforreview == 0:
                        assessmentstatus = "COMPLETED"
                        # TODO: trigger a mail to team member with retake assessment date time
                    else:
                        assessmentstatus = "PENDING FOR REVIEW"
                        # TODO: trigger a mail to reporting project manager with reviewing details
                    questions = res['Questions']
                    for q in questions:
                        qid = q['QID']
                        applicability = q['applicability']
                        options = q['options']
                        if applicability == 1:
                            scoreachieved = q['scoreachieved']
                        else:
                            scoreachieved = 0
                        totalscoreachieved = totalscoreachieved + scoreachieved
                        quesanssubmit = QuestionsAnswered(qid, applicability, options, scoreachieved, assessmentid)
                        db.session.add(quesanssubmit)
                        db.session.commit()
                    currentdt = datetime.now()
                    assessmenttakendatetime = currentdt.strftime("%H:%M:%S")
                    data = Assessment.query.filter_by(id=assessmentid).first()
                    if data is not None:
                        data.assessmentstatus = assessmentstatus
                        data.totalscoreachieved = totalscoreachieved
                        data.assessmenttakendatetime = assessmenttakendatetime
                        db.session.add(data)
                        db.session.commit()
                    return make_response(jsonify({"msg": f"Assessment submitted successfully!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@assessment.route('/api/reviewassessment', methods=['PUT'])
def reviewassessment():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
                if request.method == "PUT":
                    res = request.get_json(force=True)
                    comment = res['managerscomment']
                    if res['assessmentstatus'] == 'REJECTED':
                        assessmentstatus = 'PENDING'
                    else:
                        assessmentstatus = 'COMPLETED'  # when ACCEPTED
                        # TODO: trigger a mail to team member with retake assessment date time
                    if 'assessment_id' in res:
                        assessmentid = res['assessment_id']
                    else:
                        empid = res['emp_id']
                        projid = res['projectid']
                        areaid = res['area_id']
                        funcid = res['functionality_id']
                        if "subfunc_id" in res:
                            subfuncid = res['subfunc_id']
                            combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                        else:
                            combination = str(empid) + str(projid) + str(areaid) + str(funcid)
                        existing_assessment = Assessment.query.filter_by(combination=combination).first()
                        assessmentid = existing_assessment.id
                    currentdt = datetime.now()
                    assessmentrevieweddatetime = currentdt.strftime("%H:%M:%S")
                    data = Assessment.query.filter_by(id=assessmentid).first()
                    if data is not None:
                        data.assessmentstatus = assessmentstatus
                        data.comment = comment
                        data.assessmentrevieweddatetime = assessmentrevieweddatetime
                        db.session.add(data)
                        db.session.commit()
                    return make_response(jsonify({"msg": f"Assessment submitted successfully!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@assessment.route('/api/dashboard', methods=['POST'])
def getdashboard():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    data = Assessment.query.filter(Assessment.emp_id == emp_id)
                    results = []
                    for user in data:
                        project_data = Project.query.filter(Project.id == user.projectid).first()
                        area_data = Area.query.filter(Area.id == user.area_id).first()
                        functionality_data = Functionality.query.filter(
                            Functionality.id == user.functionality_id).first()

                        if user.subfunctionality_id is None:
                            json_data = {'assessid': user.id, 'projectid': user.projectid,
                                         'project_name': project_data.name, 'area_id': user.area_id,
                                         'area_name': area_data.name,
                                         'functionality_id': user.functionality_id,
                                         'functionality_name': functionality_data.name,
                                         'totalscoreachieved': user.totalscoreachieved,
                                         'assessmentstatus': user.assessmentstatus}
                        else:
                            subfunctionality_data = Subfunctionality.query.filter(
                                Subfunctionality.id == user.subfunctionality_id).first()
                            json_data = {'assessid': user.id, 'projectid': user.projectid,
                                         'project_name': project_data.name, 'area_id': user.area_id,
                                         'area_name': area_data.name,
                                         'functionality_id': user.functionality_id,
                                         'functionality_name': functionality_data.name,
                                         'subfunctionality_id': user.subfunctionality_id,
                                         'subfunctionality_name': subfunctionality_data.name,
                                         'totalscoreachieved': user.totalscoreachieved,
                                         'assessmentstatus': user.assessmentstatus}
                        results.append(json_data)
                    return make_response(jsonify({"data": results})), 200

            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@assessment.route('/api/assessmenttaking', methods=['POST'])
def getassessmenttaking():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
                if request.method == "POST":
                    res = request.get_json(force=True)
                    proj_id = res['proj_id']
                    area_id = res['area_id']
                    func_id = res['func_id']
                    if 'subfunc_id' in res:
                        subfunc_id = res['subfunc_id']
                        data = Question.query.filter(Question.proj_id == proj_id, Question.area_id == area_id,
                                                     Question.func_id == func_id, Question.subfunc_id == subfunc_id)
                    else:
                        data = Question.query.filter(Question.proj_id == proj_id, Question.area_id == area_id,
                                                     Question.func_id == func_id)
                    lists = []
                    for user in data:
                        lists.append(
                            {'question_id': user.id, 'question_name': user.name, 'answer_type': user.answer_type,
                             'answers': user.answers, 'maxscore': user.maxscore})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400
