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
        totalmaxscore = 0
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "PUT":
                    res = request.get_json(force=True)
                    projid = res['projectid']
                    empid = res['emp_id']
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
                        options = q['answers']
                        if applicability == 1:
                            scoreachieved = q['scoreachieved']
                            maxscore = q['maxscore']
                        else:
                            scoreachieved = 0
                            maxscore = 0
                        totalscoreachieved = totalscoreachieved + scoreachieved
                        totalmaxscore = totalmaxscore + maxscore
                        quesanssubmit = QuestionsAnswered(qid, applicability, options, scoreachieved, maxscore,
                                                          assessmentid)
                        db.session.add(quesanssubmit)
                        db.session.commit()
                    data = Assessment.query.filter_by(id=assessmentid).first()
                    if data is not None:
                        data.assessmentstatus = assessmentstatus
                        data.totalmaxscore = totalmaxscore
                        data.totalscoreachieved = totalscoreachieved
                        data.assessmenttakendatetime = datetime.now()
                        db.session.add(data)
                        db.session.commit()
                    return make_response(jsonify({"msg": f"Assessment submitted successfully!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


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
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "PUT":
                    res = request.get_json(force=True)
                    comment = res['managerscomment']
                    if res['assessmentstatus'] == 'REJECTED':
                        assessmentstatus = 'PENDING'
                    else:
                        assessmentstatus = 'COMPLETED'  # when ACCEPTED
                        # TODO: trigger a mail to team member with retake assessment date time
                    projid = res['projectid']
                    empid = res['emp_id']
                    areaid = res['area_id']
                    funcid = res['functionality_id']
                    if "subfunc_id" in res:
                        subfuncid = res['subfunc_id']
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                    else:
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid)
                    existing_assessment = Assessment.query.filter_by(combination=combination).first()
                    assessmentid = existing_assessment.id
                    data = Assessment.query.filter_by(id=assessmentid).first()
                    if data is not None:
                        data.assessmentstatus = assessmentstatus
                        data.comment = comment
                        data.assessmentrevieweddatetime = datetime.now()
                        db.session.add(data)
                        db.session.commit()
                    return make_response(jsonify({"msg": f"Thank you for reviewing the assessment!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


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
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    data = Assessment.query.filter(Assessment.emp_id == emp_id, Assessment.employeeassignedstatus == 1)
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
        return make_response(jsonify({"msg": str(e)})), 500


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
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
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
        return make_response(jsonify({"msg": str(e)})), 500


@assessment.route('/api/achievedpercentagebyteammember', methods=['POST'])
def achievedpercentagebyteammember():
    try:
        scoreachievedbytmfortheproject = 0
        maxscorefortheproject = 0
        achievedlevel = ''
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    projid = res['projectid']
                    empid = res['emp_id']
                    assessdata = Assessment.query.filter(Assessment.emp_id == empid, Assessment.projectid == projid,
                                                         Assessment.assessmentstatus == "COMPLETED")
                    for a in assessdata:
                        scoreachievedbytmfortheproject = scoreachievedbytmfortheproject + a.totalscoreachieved
                        maxscorefortheproject = maxscorefortheproject + a.totalmaxscore
                    achievedpercentage = (scoreachievedbytmfortheproject / maxscorefortheproject) * 100
                    leveldata = Project.query.filter(Project.id == projid).first()
                    for lev in leveldata.levels:
                        if (achievedpercentage >= lev['RangeFrom']) and (achievedpercentage <= lev['RangeTo']):
                            achievedlevel = lev['LevelName']
                            break
                    return make_response(jsonify({"achievedpercentage": achievedpercentage,
                                                  "achievedlevel": achievedlevel})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assessment.route('/api/assessmentcompletionbyteammember', methods=['POST'])
def assessmentcompletionbyteammember():
    try:
        countofquestionanswered = 0
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    projid = res['projectid']
                    empid = res['emp_id']
                    countofquestions = Question.query.filter_by(proj_id=projid).count()
                    assessdata = Assessment.query.filter(Assessment.emp_id == empid, Assessment.projectid == projid,
                                                         Assessment.assessmentstatus == "COMPLETED")
                    for a in assessdata:
                        cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=a.id).count()
                        countofquestionanswered = countofquestionanswered + cofquesanswdperassessment
                    assessmentcompletion = (countofquestionanswered / countofquestions) * 100
                    return make_response(jsonify({"assessmentcompletion": assessmentcompletion})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assessment.route('/api/viewuserassessmentresult', methods=['POST'])
def viewuserassessmentresult():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    projid = res['projectid']
                    empid = res['emp_id']
                    areaid = res['area_id']
                    funcid = res['functionality_id']
                    if "subfunc_id" in res:
                        subfuncid = res['subfunc_id']
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                    else:
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid)
                    assessment_data = Assessment.query.filter(Assessment.combination == combination)
                    lists = []
                    for user in assessment_data:
                        questions_answer = QuestionsAnswered.query.filter(
                            QuestionsAnswered.assignmentid == user.id).first()
                        answers_type = Question.query.filter(Question.id == questions_answer.qid).first()
                        lists.append(
                            {'answer_type': answers_type.answer_type, 'answers': questions_answer.answers,
                             'applicability': questions_answer.applicability})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
