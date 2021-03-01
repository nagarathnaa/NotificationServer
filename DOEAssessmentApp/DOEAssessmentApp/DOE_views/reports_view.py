from datetime import datetime
from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.trn_team_member_assessment_model import QuestionsAnswered
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.DOE_models.project_assignment_to_manager_model import Projectassignmenttomanager

reports = Blueprint('reports', __name__)


@reports.route('/api/achievedpercentagebyprojects', methods=['POST'])
def achievedpercentagebyprojects():
    """
        ---
        post:
          description: Achieved percentage by projects.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - getachievedpercentagebyproject
    """
    try:
        countofquestionanswered = 0
        scoreachievedfortheproject = 0
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
                    countofquestions = Question.query.filter_by(proj_id=projid).count()
                    assessment_data = Assessment.query.filter(Assessment.projectid == projid,
                                                              Assessment.assessmentstatus == "COMPLETED")
                    if assessment_data.first() is not None:
                        for data in assessment_data:
                            cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=data.id,
                                                                                          active=1).count()
                            countofquestionanswered = countofquestionanswered + cofquesanswdperassessment
                            scoreachievedfortheproject = scoreachievedfortheproject + data.totalscoreachieved
                            maxscorefortheproject = maxscorefortheproject + data.totalmaxscore
                        achievedpercentage = float(
                            "{:.2f}".format((scoreachievedfortheproject / maxscorefortheproject) * 100))
                        if countofquestions != 0:
                            assessmentcompletion = (countofquestionanswered / countofquestions) * 100
                        else:
                            assessmentcompletion = 0
                        leveldata = Project.query.filter(Project.id == projid)
                        if leveldata.first() is not None:
                            for level in leveldata.first().levels:
                                if (achievedpercentage >= level['RangeFrom']) and (
                                        achievedpercentage <= level['RangeTo']):
                                    achievedlevel = level['LevelName']
                                    break
                        else:
                            achievedlevel = None
                        project_data = Project.query.filter_by(id=projid)
                        project_data.first().assessmentcompletion = assessmentcompletion
                        project_data.first().achievedpercentage = achievedpercentage
                        project_data.first().achievedlevel = achievedlevel
                        db.session.add(project_data.first())
                        db.session.commit()
                        return make_response(jsonify({"achievedpercentage": achievedpercentage,
                                                      "achievedlevel": achievedlevel,
                                                      "assessmentcompletion": assessmentcompletion})), 200
                    else:
                        return make_response(jsonify({"msg": "No Project assessment data found!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@reports.route('/api/achievedpercentagebyarea', methods=['POST'])
def achievedpercentagebyarea():
    """
        ---
        post:
          description: Achieved percentage by areas.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - getachievedpercentagebyarea
    """
    try:
        countofquestionanswered = 0
        scoreachievedforthearea = 0
        maxscoreforthearea = 0
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
                    area_id = res['area_id']
                    countofquestions = Question.query.filter_by(proj_id=projid, area_id=area_id).count()
                    assessment_data = Assessment.query.filter(Assessment.projectid == projid,
                                                              Assessment.area_id == area_id,
                                                              Assessment.assessmentstatus == "COMPLETED")
                    if assessment_data.first() is not None:
                        for data in assessment_data:
                            cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=data.id,
                                                                                          active=1).count()
                            countofquestionanswered = countofquestionanswered + cofquesanswdperassessment
                            scoreachievedforthearea = scoreachievedforthearea + data.totalscoreachieved
                            maxscoreforthearea = maxscoreforthearea + data.totalmaxscore
                        achievedpercentage = (scoreachievedforthearea / maxscoreforthearea) * 100
                        if countofquestions != 0:
                            assessmentcompletion = (countofquestions / countofquestionanswered) * 100
                        else:
                            assessmentcompletion = 0

                        area_data = Area.query.filter_by(id=area_id)
                        area_data.first().assessmentcompletion = assessmentcompletion
                        area_data.first().achievedpercentage = achievedpercentage
                        db.session.add(area_data.first())
                        db.session.commit()
                        return make_response(jsonify({"achievedpercentage": achievedpercentage,
                                                      "assessmentcompletion": assessmentcompletion})), 200
                    else:
                        return make_response(jsonify({"msg": "No Area assessment data found!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@reports.route('/api/achievedpercentagebyfunctionality', methods=['POST'])
def achievedpercentagebyfunctionality():
    """
        ---
        post:
          description: Achieved percentage by functionality.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - getachievedpercentagebyfunctionality
    """
    try:
        countofquestionanswered = 0
        scoreachievedfortheproject = 0
        maxscorefortheproject = 0
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
                    area_id = res['area_id']
                    functionality_id = res['functionality_id']
                    countofquestions = Question.query.filter_by(proj_id=projid, area_id=area_id,
                                                                func_id=functionality_id).count()
                    assessment_data = Assessment.query.filter(Assessment.projectid == projid,
                                                              Assessment.area_id == area_id,
                                                              Assessment.functionality_id == functionality_id,
                                                              Assessment.assessmentstatus == "COMPLETED")
                    if assessment_data.first() is not None:
                        for data in assessment_data:
                            cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=data.id,
                                                                                          active=1).count()
                            countofquestionanswered = countofquestionanswered + cofquesanswdperassessment
                            scoreachievedfortheproject = scoreachievedfortheproject + data.totalscoreachieved
                            maxscorefortheproject = maxscorefortheproject + data.totalmaxscore
                        achievedpercentage = (scoreachievedfortheproject / maxscorefortheproject) * 100
                        if countofquestions != 0:
                            assessmentcompletion = (countofquestions / countofquestionanswered) * 100
                        else:
                            assessmentcompletion = 0

                        functionality_data = Functionality.query.filter_by(id=functionality_id)
                        functionality_data.first().assessmentcompletion = assessmentcompletion
                        functionality_data.first().achievedpercentage = achievedpercentage
                        db.session.add(functionality_data.first())
                        db.session.commit()
                        return make_response(jsonify({"achievedpercentage": achievedpercentage,
                                                      "assessmentcompletion": assessmentcompletion})), 200
                    else:
                        return make_response(jsonify({"msg": "No Functionality assessment data found!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
