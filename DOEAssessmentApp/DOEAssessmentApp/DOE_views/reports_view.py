from flask import *
import requests
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.trn_team_member_assessment_model import QuestionsAnswered
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

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
        assessmentcompletionforproj = 0
        achievedpercentageforproj = 0
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
                    area_data = Area.query.filter(Area.projectid == projid)
                    areacount = Area.query.filter_by(projectid=projid).count()
                    for adata in area_data:
                        my_headers = {'Authorization': 'Bearer {0}'.format(auth_token)}
                        requests.post('https://0.0.0.0:5000/api/achievedpercentagebyarea',
                                      data={'area_id': adata.id,
                                            'projectid': projid}, headers=my_headers)
                        assessmentcompletionforproj = assessmentcompletionforproj + adata.assessmentcompletion
                        achievedpercentageforproj = achievedpercentageforproj + adata.achievedpercentage
                    assessmentcompletion = assessmentcompletionforproj / areacount
                    achievedpercentage = achievedpercentageforproj / areacount
                    project_data = Project.query.filter_by(id=projid)
                    project_data.first().assessmentcompletion = assessmentcompletion
                    project_data.first().achievedpercentage = achievedpercentage
                    leveldata = Project.query.filter(Project.id == projid)
                    if leveldata.first() is not None:
                        for level in leveldata.first().levels:
                            if (achievedpercentage >= level['RangeFrom']) and (
                                    achievedpercentage <= level['RangeTo']):
                                achievedlevel = level['LevelName']
                                break
                    else:
                        achievedlevel = ''
                    project_data.first().achievedlevel = achievedlevel
                    db.session.add(project_data.first())
                    db.session.commit()
                    return make_response(jsonify({"achievedpercentage": str(achievedpercentage),
                                                  "achievedlevel": achievedlevel,
                                                  "assessmentcompletion": str(assessmentcompletion)})), 200
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
        assessmentcompletionforarea = 0
        achievedpercentageforarea = 0
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
                    area_id = res['area_id']
                    functionality_data = Functionality.query.filter(Functionality.proj_id == projid,
                                                                    Functionality.area_id == area_id)
                    funccount = Functionality.query.filter_by(proj_id=projid,
                                                              area_id=area_id).count()
                    for fdata in functionality_data:
                        my_headers = {'Authorization': 'Bearer {0}'.format(auth_token)}
                        requests.post('https://0.0.0.0:5000/api/achievedpercentagebyfunctionality',
                                      data={'functionality_id': fdata.id,
                                            'area_id': area_id,
                                            'projectid': projid}, headers=my_headers)
                        assessmentcompletionforarea = assessmentcompletionforarea + fdata.assessmentcompletion
                        achievedpercentageforarea = achievedpercentageforarea + fdata.achievedpercentage
                    assessmentcompletion = assessmentcompletionforarea / funccount
                    achievedpercentage = achievedpercentageforarea / funccount
                    area_data = Area.query.filter_by(id=area_id)
                    area_data.first().assessmentcompletion = assessmentcompletion
                    area_data.first().achievedpercentage = achievedpercentage
                    leveldata = Project.query.filter(Project.id == projid)
                    if leveldata.first() is not None:
                        for level in leveldata.first().levels:
                            if (achievedpercentage >= level['RangeFrom']) and (
                                    achievedpercentage <= level['RangeTo']):
                                achievedlevel = level['LevelName']
                                break
                    else:
                        achievedlevel = ''
                    area_data.first().achievedlevel = achievedlevel
                    db.session.add(area_data.first())
                    db.session.commit()
                    return make_response(jsonify({"achievedpercentage": str(achievedpercentage),
                                                  "assessmentcompletion": str(assessmentcompletion),
                                                  "achievedlevel": achievedlevel})), 200
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
        assessmentcompletionforfunc = 0
        achievedpercentageforfunc = 0
        countofquestionanswered = 0
        scoreachievedforthefunc = 0
        countofquestions = 0
        maxscoreforthefunc = 0
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
                    area_id = res['area_id']
                    functionality_id = res['functionality_id']
                    # region 'when assessment not assigned to sub-functionality and directly to functionality
                    assessment_data = Assessment.query.filter(Assessment.projectid == projid,
                                                              Assessment.area_id == area_id,
                                                              Assessment.functionality_id == functionality_id,
                                                              Assessment.subfunctionality_id is None,
                                                              Assessment.assessmentstatus == "COMPLETED",
                                                              Assessment.active == 1)
                    usercount = Assessment.query.filter_by(projectid=projid,
                                                           area_id=area_id,
                                                           functionality_id=functionality_id,
                                                           subfunctionality_id=None,
                                                           assessmentstatus="COMPLETED",
                                                           active=1).count()
                    if assessment_data.first() is not None:
                        for data in assessment_data:
                            countofquestions = countofquestions + data.countoftotalquestions
                            cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=data.id,
                                                                                          active=1,
                                                                                          applicability=1).count()
                            countofquestionanswered = countofquestionanswered + cofquesanswdperassessment
                            scoreachievedforthefunc = scoreachievedforthefunc + data.totalscoreachieved
                            maxscoreforthefunc = maxscoreforthefunc + data.totalmaxscore
                        if countofquestions != 0:
                            assessmentcompletion = ((countofquestionanswered / usercount) / countofquestions) * 100
                            achievedpercentage = (scoreachievedforthefunc / maxscoreforthefunc) * 100
                        else:
                            assessmentcompletion = 0
                            achievedpercentage = 0
                        functionality_data = Functionality.query.filter_by(id=functionality_id)
                        leveldata = Project.query.filter(Project.id == functionality_data.first().proj_id)
                        if leveldata.first() is not None:
                            for level in leveldata.first().levels:
                                if (achievedpercentage >= level['RangeFrom']) and (
                                        achievedpercentage <= level['RangeTo']):
                                    achievedlevel = level['LevelName']
                                    break
                        else:
                            achievedlevel = ''
                        functionality_data.first().assessmentcompletion = assessmentcompletion
                        functionality_data.first().achievedpercentage = achievedpercentage
                        functionality_data.first().achievedlevel = achievedlevel
                        db.session.add(functionality_data.first())
                        db.session.commit()
                        return make_response(jsonify({"achievedpercentage": str(achievedpercentage),
                                                      "assessmentcompletion": str(assessmentcompletion),
                                                      "achievedlevel": achievedlevel})), 200
                    else:
                        subfunctionality_data = Subfunctionality.query.filter(Subfunctionality.proj_id == projid,
                                                                              Subfunctionality.area_id == area_id,
                                                                              Subfunctionality.func_id ==
                                                                              functionality_id)
                        subfunccount = Subfunctionality.query.filter_by(proj_id=projid,
                                                                        area_id=area_id,
                                                                        func_id=functionality_id).count()
                        for sfdata in subfunctionality_data:
                            my_headers = {'Authorization': 'Bearer {0}'.format(auth_token)}
                            requests.post('https://0.0.0.0:5000/api/achievedpercentagebysubfunctionality',
                                          data={'subfunc_id': sfdata.id,
                                                'functionality_id': functionality_id,
                                                'area_id': area_id,
                                                'projectid': projid}, headers=my_headers)
                            assessmentcompletionforfunc = assessmentcompletionforfunc + sfdata.assessmentcompletion
                            achievedpercentageforfunc = achievedpercentageforfunc + sfdata.achievedpercentage
                        assessmentcompletion = assessmentcompletionforfunc / subfunccount
                        achievedpercentage = achievedpercentageforfunc / subfunccount
                        functionality_data = Functionality.query.filter_by(id=functionality_id)
                        leveldata = Project.query.filter(Project.id == functionality_data.first().proj_id)
                        if leveldata.first() is not None:
                            for level in leveldata.first().levels:
                                if (achievedpercentage >= level['RangeFrom']) and (
                                        achievedpercentage <= level['RangeTo']):
                                    achievedlevel = level['LevelName']
                                    break
                        else:
                            achievedlevel = ''
                        functionality_data.first().assessmentcompletion = assessmentcompletion
                        functionality_data.first().achievedpercentage = achievedpercentage
                        functionality_data.first().achievedlevel = achievedlevel
                        db.session.add(functionality_data.first())
                        db.session.commit()
                        return make_response(jsonify({"achievedpercentage": str(achievedpercentage),
                                                      "assessmentcompletion": str(assessmentcompletion),
                                                      "achievedlevel": achievedlevel})), 200
                        # return make_response(jsonify({"msg": "No Functionality assessment data found!!"})), 200
                    # end region
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@reports.route('/api/achievedpercentagebysubfunctionality', methods=['POST'])
def achievedpercentagebysubfunctionality():
    try:
        countofquestionanswered = 0
        scoreachievedforthefunc = 0
        countofquestions = 0
        maxscoreforthefunc = 0
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
                    area_id = res['area_id']
                    functionality_id = res['functionality_id']
                    subfunc_id = res['subfunc_id']
                    assessment_data = Assessment.query.filter(Assessment.projectid == projid,
                                                              Assessment.area_id == area_id,
                                                              Assessment.functionality_id == functionality_id,
                                                              Assessment.subfunctionality_id == subfunc_id,
                                                              Assessment.assessmentstatus == "COMPLETED",
                                                              Assessment.active == 1)
                    usercount = Assessment.query.filter_by(projectid=projid,
                                                           area_id=area_id,
                                                           functionality_id=functionality_id,
                                                           subfunctionality_id=subfunc_id,
                                                           assessmentstatus="COMPLETED",
                                                           active=1).count()
                    if assessment_data.first() is not None:
                        for data in assessment_data:
                            countofquestions = countofquestions + data.countoftotalquestions
                            cofquesanswdperassessment = QuestionsAnswered.query.filter_by(assignmentid=data.id,
                                                                                          active=1,
                                                                                          applicability=1).count()
                            countofquestionanswered = countofquestionanswered + cofquesanswdperassessment
                            scoreachievedforthefunc = scoreachievedforthefunc + data.totalscoreachieved
                            maxscoreforthefunc = maxscoreforthefunc + data.totalmaxscore
                        if countofquestions != 0:
                            assessmentcompletion = ((countofquestionanswered / usercount) / countofquestions) * 100
                            achievedpercentage = (scoreachievedforthefunc / maxscoreforthefunc) * 100
                        else:
                            assessmentcompletion = 0
                            achievedpercentage = 0
                        subfunctionality_data = Subfunctionality.query.filter_by(id=subfunc_id)
                        leveldata = Project.query.filter(Project.id == subfunctionality_data.first().proj_id)
                        if leveldata.first() is not None:
                            for level in leveldata.first().levels:
                                if (achievedpercentage >= level['RangeFrom']) and (
                                        achievedpercentage <= level['RangeTo']):
                                    achievedlevel = level['LevelName']
                                    break
                        else:
                            achievedlevel = ''
                        subfunctionality_data.first().assessmentcompletion = assessmentcompletion
                        subfunctionality_data.first().achievedpercentage = achievedpercentage
                        subfunctionality_data.first().achievedlevel = achievedlevel
                        db.session.add(subfunctionality_data.first())
                        db.session.commit()
                        return make_response(jsonify({"achievedpercentage": str(achievedpercentage),
                                                      "assessmentcompletion": str(assessmentcompletion),
                                                      "achievedlevel": achievedlevel})), 200
                    else:
                        return make_response(jsonify({"msg": "No Sub-functionality assessment data found!!"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
