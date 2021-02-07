import datetime
from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.project_assignment_to_manager_model import Projectassignmenttomanager
from DOEAssessmentApp.DOE_models.trn_team_member_assessment_model import QuestionsAnswered
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.email_configuration_model import Emailconfiguration
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.smtp_integration import *

assessment = Blueprint('assessment', __name__)


@assessment.route('/api/submitassessment', methods=['PUT'])
def submitassessment():
    try:
        totalscoreachieved = 0
        totalmaxscore = 0
        retakedatetime = None
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
                    managerdata = Projectassignmenttomanager.query.filter_by(project_id=projid, status=1).first()
                    empid = res['emp_id']
                    userdata = Companyuserdetails.query.filter_by(empid=empid).first()
                    empname = userdata.empname
                    companyid = userdata.companyid
                    mailto = userdata.empemail
                    emailconf = Emailconfiguration.query.filter_by(companyid=companyid).first()
                    if emailconf.email == 'default' and emailconf.host == 'default' \
                            and emailconf.password == 'default':
                        mailfrom = app.config.get('FROM_EMAIL')
                        host = app.config.get('HOST')
                        pwd = app.config.get('PWD')
                    else:
                        mailfrom = emailconf.email
                        host = emailconf.host
                        pwd = emailconf.password
                    areaid = res['area_id']
                    funcid = res['functionality_id']
                    if "subfunc_id" in res:
                        subfuncid = res['subfunc_id']
                        dataforretake = Subfunctionality.query.filter_by(id=subfuncid).first()
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                    else:
                        dataforretake = Functionality.query.filter_by(id=funcid).first()
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid)
                    existing_assessment = Assessment.query.filter_by(combination=combination).first()
                    assessmentid = existing_assessment.id
                    checkifeligibledata = Assessment.query.filter_by(id=assessmentid).first()
                    if checkifeligibledata.assessmentretakedatetime is not None and \
                            (checkifeligibledata.assessmentretakedatetime.replace(microsecond=0) -
                             datetime.datetime.now().replace(microsecond=0)).total_seconds() > 0:
                        return make_response(jsonify({"msg": f"Your are not allowed to take the assessment "
                                                             f"now!! Please take it on "
                                                             + str(checkifeligibledata.assessmentretakedatetime.
                                                                   replace(microsecond=0))})), 200
                    else:
                        data_proj = Project.query.filter_by(id=projid).first()
                        assessmenttakendatetime = datetime.datetime.now()
                        if data_proj.needforreview == 0:
                            assessmentstatus = "COMPLETED"
                            # triggering a mail to team member with retake assessment date time
                            rah = dataforretake.retake_assessment_days
                            hours_added = datetime.timedelta(hours=rah)
                            retakedatetime = assessmenttakendatetime + hours_added
                            mailsubject = 'SUBMITTED: Congratulations!! Assessment completed successfully.'
                            mailbody = 'Thank you for taking the assessment!! You can retake it on ' \
                                       + str(retakedatetime.replace(microsecond=0)) + "."
                            # mailout = trigger_mail(mailfrom, mailto, host, pwd, mailsubject, empname, mailbody)
                            # print(mailout)
                            # TODO: trigger a mail to the project Manager
                        else:
                            assessmentstatus = "PENDING FOR REVIEW"
                            # triggering a mail to team member to notify that the assessment submitted has
                            # gone for review
                            mailsubject = 'IN REVIEW: Congratulations!! Assessment submitted successfully but pending' \
                                          ' for review'
                            mailbody = 'Thank you for taking the assessment!! It is pending with your reporting ' \
                                       'manager to review.'
                            # mailout = trigger_mail(mailfrom, mailto, host, pwd, mailsubject, empname, mailbody)
                            # print(mailout)
                            # triggering a mail to reporting project manager with reviewing details
                            userdata = Companyuserdetails.query.filter_by(empid=managerdata.emp_id).first()
                            mailto = userdata.empemail
                            mailtoname = userdata.empname
                            mailsubject = "Assessment review of " + empname
                            mailbody = empname + ' has taken the assessment and its pending for your review.'
                            # mailout = trigger_mail(mailfrom, mailto, host, pwd, mailsubject, mailtoname, mailbody)
                            # print(mailout)
                        qadata = QuestionsAnswered.query.filter_by(assignmentid=assessmentid)
                        if qadata.first() is not None:
                            for qa in qadata:
                                eachqadata = QuestionsAnswered.query.filter_by(id=qa.id).first()
                                eachqadata.active = 0
                                db.session.add(eachqadata)
                                db.session.commit()
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
                            data.comment = None
                            data.totalmaxscore = totalmaxscore
                            data.totalscoreachieved = totalscoreachieved
                            data.assessmenttakendatetime = assessmenttakendatetime
                            data.assessmentretakedatetime = retakedatetime
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
        retakedatetime = None
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
                    projid = res['projectid']
                    empid = res['emp_id']
                    userdata = Companyuserdetails.query.filter_by(empid=empid).first()
                    empname = userdata.empname
                    companyid = userdata.companyid
                    mailto = userdata.empemail
                    emailconf = Emailconfiguration.query.filter_by(companyid=companyid).first()
                    if emailconf.email == 'default' and emailconf.host == 'default' \
                            and emailconf.password == 'default':
                        mailfrom = app.config.get('FROM_EMAIL')
                        host = app.config.get('HOST')
                        pwd = app.config.get('PWD')
                    else:
                        mailfrom = emailconf.email
                        host = emailconf.host
                        pwd = emailconf.password
                    areaid = res['area_id']
                    funcid = res['functionality_id']
                    if "subfunc_id" in res:
                        subfuncid = res['subfunc_id']
                        dataforretake = Subfunctionality.query.filter_by(id=subfuncid).first()
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
                    else:
                        dataforretake = Functionality.query.filter_by(id=funcid).first()
                        combination = str(empid) + str(projid) + str(areaid) + str(funcid)
                    existing_assessment = Assessment.query.filter_by(combination=combination).first()
                    assessmentid = existing_assessment.id
                    data = Assessment.query.filter_by(id=assessmentid).first()
                    if res['assessmentstatus'] == 'REJECTED':
                        assessmentstatus = 'PENDING'
                        # triggering a mail to team member to notify that the assessment submitted has been rejected
                        mailsubject = 'REVIEWED: Regrets!! Assessment has been rejected.'
                        mailbody = 'The assessment submitted by you has been rejected by your reporting manager!!' \
                                   ' Please retake the assessment and submit it once again.'
                        # mailout = trigger_mail(mailfrom, mailto, host, pwd, mailsubject, empname, mailbody)
                        # print(mailout)
                    else:
                        assessmentstatus = 'COMPLETED'  # when ACCEPTED
                        # triggering a mail to team member with retake assessment date time
                        rah = dataforretake.retake_assessment_days
                        hours_added = datetime.timedelta(hours=rah)
                        retakedatetime = data.assessmenttakendatetime + hours_added
                        mailsubject = 'REVIEWED: Congratulations!! Assessment has been accepted.'
                        mailbody = 'The assessment submitted by you has been accepted by your reporting ' \
                                   'manager!! You can retake it on ' + str(retakedatetime.replace(microsecond=0)) + "."
                        # mailout = trigger_mail(mailfrom, mailto, host, pwd, mailsubject, empname, mailbody)
                        # print(mailout)
                    if data is not None:
                        data.assessmentstatus = assessmentstatus
                        data.comment = comment
                        data.assessmentrevieweddatetime = datetime.datetime.now()
                        data.assessmentretakedatetime = retakedatetime
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
                                         'assessmentstatus': user.assessmentstatus,
                                         'comment': user.comment,
                                         'retakedatetime': user.assessmentretakedatetime}
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
                                         'assessmentstatus': user.assessmentstatus,
                                         'comment': user.comment,
                                         'retakedatetime': user.assessmentretakedatetime}
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
                        cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=a.id,
                                                                                      active=1).count()
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
                    assessment_data = Assessment.query.filter_by(combination=combination).first()
                    questions_answer = QuestionsAnswered.query.filter_by(assignmentid=assessment_data.id, active=1).all()
                    lists = []
                    for user in questions_answer:
                        answers_type = Question.query.filter(Question.id == user.qid).first()
                        lists.append(
                            {'question_id': user.qid, 'question_name': answers_type.name,
                             'questions_answers': user.answers,
                             'scoreachieved': user.scoreachieved, 'answer_type': answers_type.answer_type,
                             'applicability': user.applicability})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
