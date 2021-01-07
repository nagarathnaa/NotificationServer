import xlrd
from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.company_details_model import Companydetails

project = Blueprint('project', __name__)

colsproject = ['id', 'name', 'description', 'levels', 'companyid', 'assessmentcompletion', 'achievedpercentage',
               'needforreview', 'creationdatetime', 'updationdatetime']


@project.route('/api/project', methods=['GET', 'POST'])
def getaddproject():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    data = Project.query.all()
                    result = [{col: getattr(d, col) for col in colsproject} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    defaultdatarequired = res['defaultdatarequired']
                    projname = res['ProjectName']
                    projdesc = res['ProjectDescription']
                    comp_id = res['CompanyID']
                    levels = res['Levels']
                    if 'NeedForReview' in res:
                        nfr = res['NeedForReview']
                    else:
                        nfr = 1
                    existing_project = Project.query.filter(Project.name == projname,
                                                            Project.companyid == comp_id).one_or_none()
                    if existing_project is None:
                        projins = Project(projname, projdesc, levels, comp_id, nfr)
                        db.session.add(projins)
                        db.session.commit()
                        data = Project.query.filter_by(id=projins.id)
                        result = [{col: getattr(d, col) for col in colsproject} for d in data]
                        if defaultdatarequired == 1:
                            wb = xlrd.open_workbook('static/defaultdata.xlsx')
                            sh = wb.sheet_by_name('Sheet2')
                            for i in range(1, sh.nrows):
                                existing_area = Area.query.filter(Area.name == sh.cell_value(i, 0),
                                                                  Area.projectid == projins.id).one_or_none()
                                if existing_area is None:
                                    areains = Area(sh.cell_value(i, 0), sh.cell_value(i, 1), projins.id)
                                    db.session.add(areains)
                                    db.session.commit()
                                findareadata = Area.query.filter_by(name=sh.cell_value(i, 0),
                                                                    projectid=projins.id).first()
                                existing_functionality = Functionality.query.filter(
                                    Functionality.name == sh.cell_value(i, 2),
                                    Functionality.area_id ==
                                    findareadata.id).one_or_none()
                                if existing_functionality is None:
                                    funcins = Functionality(sh.cell_value(i, 2),
                                                            sh.cell_value(i, 3),
                                                            sh.cell_value(i, 6) if sh.cell_value(i, 4) == '' else None,
                                                            findareadata.id, projins.id)
                                    db.session.add(funcins)
                                    db.session.commit()
                                if sh.cell_value(i, 4) != '':
                                    findfuncdata = Functionality.query.filter_by(
                                        name=sh.cell_value(i, 2),
                                        area_id=findareadata.id).first()
                                    existing_subfunctionality = Subfunctionality.query.filter(
                                        Subfunctionality.name ==
                                        sh.cell_value(i, 4),
                                        Subfunctionality.func_id ==
                                        findfuncdata.id).one_or_none()
                                    if existing_subfunctionality is None:
                                        subfuncins = Subfunctionality(sh.cell_value(i, 4),
                                                                      sh.cell_value(i, 5),
                                                                      sh.cell_value(i, 6),
                                                                      findfuncdata.id, findareadata.id, projins.id)
                                        db.session.add(subfuncins)
                                        db.session.commit()
                                        # add question in sub func
                                        combination = str(projins.id) + str(findareadata.id) + str(
                                            findfuncdata.id) + str(subfuncins.id) + str(sh.cell_value(i, 8))
                                        existing_question = Question.query.filter(
                                            Question.combination == combination).one_or_none()
                                        if existing_question is None:
                                            maxscore = 0
                                            answers = None
                                            if sh.cell_value(i, 9) == 'Yes / No':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 10),
                                                        "score": sh.cell_value(i, 11),
                                                        "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                        sh.cell_value(i, 12)
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 13),
                                                        "score": sh.cell_value(i, 14),
                                                        "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                        sh.cell_value(i, 15)
                                                    }
                                                ]
                                                maxscore = max(int(sh.cell_value(i, 11)), int(sh.cell_value(i, 14)))
                                            elif sh.cell_value(i, 9) == 'Multi choice':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 10),
                                                        "score": sh.cell_value(i, 11),
                                                        "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                        sh.cell_value(i, 12)
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 13),
                                                        "score": sh.cell_value(i, 14),
                                                        "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                        sh.cell_value(i, 15)
                                                    },
                                                    {
                                                        "option3": sh.cell_value(i, 16),
                                                        "score": sh.cell_value(i, 17),
                                                        "childquestionid": 0 if sh.cell_value(i, 18) == '' else
                                                        sh.cell_value(i, 18)
                                                    },
                                                    {
                                                        "option4": sh.cell_value(i, 19),
                                                        "score": sh.cell_value(i, 20),
                                                        "childquestionid": 0 if sh.cell_value(i, 21) == '' else
                                                        sh.cell_value(i, 21)
                                                    }
                                                ]
                                                maxscore = int(sh.cell_value(i, 11)) + int(sh.cell_value(i, 14)) + int(
                                                    sh.cell_value(i, 17)) + int(sh.cell_value(i, 20))
                                            elif sh.cell_value(i, 9) == 'Single choice':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 10),
                                                        "score": sh.cell_value(i, 11),
                                                        "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                        sh.cell_value(i, 12)
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 13),
                                                        "score": sh.cell_value(i, 14),
                                                        "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                        sh.cell_value(i, 15)
                                                    },
                                                    {
                                                        "option3": sh.cell_value(i, 16),
                                                        "score": sh.cell_value(i, 17),
                                                        "childquestionid": 0 if sh.cell_value(i, 18) == '' else
                                                        sh.cell_value(i, 18)
                                                    },
                                                    {
                                                        "option4": sh.cell_value(i, 19),
                                                        "score": sh.cell_value(i, 20),
                                                        "childquestionid": 0 if sh.cell_value(i, 21) == '' else
                                                        sh.cell_value(i, 21)
                                                    }
                                                ]
                                                maxscore = max(int(sh.cell_value(i, 11)), int(sh.cell_value(i, 14)),
                                                               int(sh.cell_value(i, 17)), int(sh.cell_value(i, 20)))
                                            quesins = Question(sh.cell_value(i, 8), sh.cell_value(i, 9), answers,
                                                               maxscore,
                                                               subfuncins.id,
                                                               findfuncdata.id, findareadata.id, projins.id,
                                                               combination)
                                            db.session.add(quesins)
                                            db.session.commit()
                                        else:
                                            pass
                                    else:
                                        # add questions in sub func
                                        findsubfuncdata = Subfunctionality.query.filter(Subfunctionality.name ==
                                                                                        sh.cell_value(i, 4),
                                                                                        Subfunctionality.func_id ==
                                                                                        findfuncdata.id).one_or_none()
                                        combination = str(projins.id) + str(findareadata.id) + str(
                                            findfuncdata.id) + str(findsubfuncdata.id) + str(sh.cell_value(i, 8))
                                        existing_question = Question.query.filter(
                                            Question.combination == combination).one_or_none()
                                        if existing_question is None:
                                            maxscore = 0
                                            answers = None
                                            if sh.cell_value(i, 9) == 'Yes / No':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 10),
                                                        "score": sh.cell_value(i, 11),
                                                        "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                        sh.cell_value(i, 12)
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 13),
                                                        "score": sh.cell_value(i, 14),
                                                        "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                        sh.cell_value(i, 15)
                                                    }
                                                ]
                                                maxscore = max(int(sh.cell_value(i, 11)), int(sh.cell_value(i, 14)))
                                            elif sh.cell_value(i, 9) == 'Multi choice':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 10),
                                                        "score": sh.cell_value(i, 11),
                                                        "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                        sh.cell_value(i, 12)
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 13),
                                                        "score": sh.cell_value(i, 14),
                                                        "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                        sh.cell_value(i, 15)
                                                    },
                                                    {
                                                        "option3": sh.cell_value(i, 16),
                                                        "score": sh.cell_value(i, 17),
                                                        "childquestionid": 0 if sh.cell_value(i, 18) == '' else
                                                        sh.cell_value(i, 18)
                                                    },
                                                    {
                                                        "option4": sh.cell_value(i, 19),
                                                        "score": sh.cell_value(i, 20),
                                                        "childquestionid": 0 if sh.cell_value(i, 21) == '' else
                                                        sh.cell_value(i, 21)
                                                    }
                                                ]
                                                maxscore = int(sh.cell_value(i, 11)) + int(sh.cell_value(i, 14)) + int(
                                                    sh.cell_value(i, 17)) + int(sh.cell_value(i, 20))
                                            elif sh.cell_value(i, 9) == 'Single choice':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 10),
                                                        "score": sh.cell_value(i, 11),
                                                        "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                        sh.cell_value(i, 12)
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 13),
                                                        "score": sh.cell_value(i, 14),
                                                        "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                        sh.cell_value(i, 15)
                                                    },
                                                    {
                                                        "option3": sh.cell_value(i, 16),
                                                        "score": sh.cell_value(i, 17),
                                                        "childquestionid": 0 if sh.cell_value(i, 18) == '' else
                                                        sh.cell_value(i, 18)
                                                    },
                                                    {
                                                        "option4": sh.cell_value(i, 19),
                                                        "score": sh.cell_value(i, 20),
                                                        "childquestionid": 0 if sh.cell_value(i, 21) == '' else
                                                        sh.cell_value(i, 21)
                                                    }
                                                ]
                                                maxscore = max(int(sh.cell_value(i, 11)), int(sh.cell_value(i, 14)),
                                                               int(sh.cell_value(i, 17)), int(sh.cell_value(i, 20)))
                                            quesins = Question(sh.cell_value(i, 8), sh.cell_value(i, 9), answers,
                                                               maxscore,
                                                               findsubfuncdata.id,
                                                               findfuncdata.id, findareadata.id, projins.id,
                                                               combination)
                                            db.session.add(quesins)
                                            db.session.commit()
                                else:
                                    # add questions in func
                                    findfuncdata = Functionality.query.filter_by(
                                        name=sh.cell_value(i, 2),
                                        area_id=findareadata.id).first()
                                    combination = str(projins.id) + str(findareadata.id) + str(
                                        findfuncdata.id) + str(sh.cell_value(i, 8))
                                    existing_question = Question.query.filter(
                                        Question.combination == combination).one_or_none()
                                    if existing_question is None:
                                        maxscore = 0
                                        answers = None
                                        if sh.cell_value(i, 9) == 'Yes / No':
                                            answers = [
                                                {
                                                    "option1": sh.cell_value(i, 10),
                                                    "score": sh.cell_value(i, 11),
                                                    "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                    sh.cell_value(i, 12)
                                                },
                                                {
                                                    "option2": sh.cell_value(i, 13),
                                                    "score": sh.cell_value(i, 14),
                                                    "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                    sh.cell_value(i, 15)
                                                }
                                            ]
                                            maxscore = max(int(sh.cell_value(i, 11)), int(sh.cell_value(i, 14)))
                                        elif sh.cell_value(i, 9) == 'Multi choice':
                                            answers = [
                                                {
                                                    "option1": sh.cell_value(i, 10),
                                                    "score": sh.cell_value(i, 11),
                                                    "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                    sh.cell_value(i, 12)
                                                },
                                                {
                                                    "option2": sh.cell_value(i, 13),
                                                    "score": sh.cell_value(i, 14),
                                                    "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                    sh.cell_value(i, 15)
                                                },
                                                {
                                                    "option3": sh.cell_value(i, 16),
                                                    "score": sh.cell_value(i, 17),
                                                    "childquestionid": 0 if sh.cell_value(i, 18) == '' else
                                                    sh.cell_value(i, 18)
                                                },
                                                {
                                                    "option4": sh.cell_value(i, 19),
                                                    "score": sh.cell_value(i, 20),
                                                    "childquestionid": 0 if sh.cell_value(i, 21) == '' else
                                                    sh.cell_value(i, 21)
                                                }
                                            ]
                                            maxscore = int(sh.cell_value(i, 11)) + int(sh.cell_value(i, 14)) + int(
                                                sh.cell_value(i, 17)) + int(sh.cell_value(i, 20))
                                        elif sh.cell_value(i, 9) == 'Single choice':
                                            answers = [
                                                {
                                                    "option1": sh.cell_value(i, 10),
                                                    "score": sh.cell_value(i, 11),
                                                    "childquestionid": 0 if sh.cell_value(i, 12) == '' else
                                                    sh.cell_value(i, 12)
                                                },
                                                {
                                                    "option2": sh.cell_value(i, 13),
                                                    "score": sh.cell_value(i, 14),
                                                    "childquestionid": 0 if sh.cell_value(i, 15) == '' else
                                                    sh.cell_value(i, 15)
                                                },
                                                {
                                                    "option3": sh.cell_value(i, 16),
                                                    "score": sh.cell_value(i, 17),
                                                    "childquestionid": 0 if sh.cell_value(i, 18) == '' else
                                                    sh.cell_value(i, 18)
                                                },
                                                {
                                                    "option4": sh.cell_value(i, 19),
                                                    "score": sh.cell_value(i, 20),
                                                    "childquestionid": 0 if sh.cell_value(i, 21) == '' else
                                                    sh.cell_value(i, 21)
                                                }
                                            ]
                                            maxscore = max(int(sh.cell_value(i, 11)), int(sh.cell_value(i, 14)),
                                                           int(sh.cell_value(i, 17)), int(sh.cell_value(i, 20)))
                                        quesins = Question(sh.cell_value(i, 8), sh.cell_value(i, 9), answers,
                                                           maxscore,
                                                           None,
                                                           findfuncdata.id, findareadata.id, projins.id,
                                                           combination)
                                        db.session.add(quesins)
                                        db.session.commit()
                            return make_response(jsonify({"message": f"Project {projname} successfully inserted with "
                                                                     f"default assessments.",
                                                          "data": result[0]})), 201
                        else:
                            return make_response(jsonify({"message": f"Project {projname} successfully inserted.",
                                                          "data": result[0]})), 201
                    else:
                        data_comp = Companydetails.query.filter_by(id=comp_id).first()
                        return make_response(jsonify({"message": f"Project {projname} already exists for company "
                                                                 f"{data_comp.companyname}."})), 400
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@project.route('/api/updelproject/', methods=['POST', 'PUT', 'DELETE'])
def updelproject():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                res = request.get_json(force=True)
                projid = res['projectid']
                data = Project.query.filter_by(id=projid)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'POST':
                        result = [{col: getattr(d, col) for col in colsproject} for d in data]
                        return make_response(jsonify({"data": result[0]})), 200
                    elif request.method == 'PUT':
                        projectname = res['ProjectName']
                        compid = res['CompanyID']
                        levels = res['Levels']
                        if 'NeedForReview' in res:
                            nfr = res['NeedForReview']
                        else:
                            nfr = 1
                        existing_project = Project.query.filter(Project.name == projectname,
                                                                Project.companyid == compid).one_or_none()
                        data.first().levels = levels
                        data.first().needforreview = nfr
                        if existing_project is None:
                            data.first().name = projectname
                            db.session.add(data.first())
                            db.session.commit()
                            return make_response(jsonify({"message": f"Project {projectname} "
                                                                     f"successfully updated."})), 200
                        else:
                            db.session.add(data.first())
                            db.session.commit()
                            data_comp = Companydetails.query.filter_by(id=compid).first()
                            return make_response(jsonify({"message": f"Project {projectname} already exists for company"
                                                                     f" {data_comp.companyname}."})), 400
                    elif request.method == 'DELETE':
                        db.session.delete(data.first())
                        db.session.commit()
                        data_area = Area.query.filter_by(projectid=projid)
                        if data_area is not None:
                            for a in data_area:
                                db.session.delete(a)
                                db.session.commit()
                        data_func = Functionality.query.filter_by(proj_id=projid)
                        if data_func is not None:
                            for f in data_func:
                                db.session.delete(f)
                                db.session.commit()
                        data_subfunc = Subfunctionality.query.filter_by(proj_id=projid)
                        if data_subfunc is not None:
                            for s in data_subfunc:
                                db.session.delete(s)
                                db.session.commit()
                        data_question = Question.query.filter_by(proj_id=projid)
                        if data_question is not None:
                            for q in data_question:
                                db.session.delete(q)
                                db.session.commit()
                        return make_response(jsonify({"message": f"Project with ID {projid} "
                                                                 f"successfully deleted."})), 204
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
