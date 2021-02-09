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
    """
        ---
        get:
          description: Fetch project(s).
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - getcreateproject
        post:
          description: Create a project.
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
              - getcreateproject
    """
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
                    if 'excelfordefaultquestions' in res:
                        excelfordefaultquestions = res['excelfordefaultquestions']
                    else:
                        excelfordefaultquestions = None
                    projname = res['name']
                    projdesc = res['description']
                    comp_id = res['companyid']
                    levels = res['levels']
                    if 'needforreview' in res:
                        nfr = res['needforreview']
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
                        if excelfordefaultquestions is not None:
                            wb = xlrd.open_workbook('static/' + excelfordefaultquestions + '.xlsx')
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
                                        # add question in new sub func
                                        combination = str(projins.id) + str(findareadata.id) + str(
                                            findfuncdata.id) + str(subfuncins.id) + str(sh.cell_value(i, 7))
                                        existing_question = Question.query.filter(
                                            Question.combination == combination).one_or_none()
                                        if existing_question is None:
                                            maxscore = 0
                                            answers = []
                                            if sh.cell_value(i, 8) == 'Yes / No':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 9),
                                                        "score": sh.cell_value(i, 10),
                                                        "childquestionid": [
                                                            Question.query.filter_by(name=child).first().id for child in
                                                            sh.cell_value(i, 11).split(',') if Question.query.filter_by(
                                                                name=child) is not None] if ',' in sh.cell_value(i, 11)
                                                        else 0 if Question.query.filter_by(
                                                            name=sh.cell_value(i, 11)) is None else
                                                        Question.query.filter_by(name=sh.cell_value(i, 11)).first().id
                                                        if sh.cell_value(i, 11) != ''
                                                        else 0
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 12),
                                                        "score": sh.cell_value(i, 13),
                                                        "childquestionid": [
                                                            Question.query.filter_by(name=child).first().id for child in
                                                            sh.cell_value(i, 14).split(',') if Question.query.filter_by(
                                                                name=child) is not None] if ',' in sh.cell_value(i, 14)
                                                        else 0 if Question.query.filter_by(
                                                            name=sh.cell_value(i, 14)) is None else
                                                        Question.query.filter_by(name=sh.cell_value(i, 14)).first().id
                                                        if sh.cell_value(i, 14) != ''
                                                        else 0
                                                    }
                                                ]
                                                maxscore = max(int(sh.cell_value(i, 10)), int(sh.cell_value(i, 13)))
                                            elif sh.cell_value(i, 8) == 'Multi choice':
                                                k = 1
                                                for j in range(9, sh.ncols, 3):
                                                    if sh.cell_value(i, j) != '':
                                                        answers.append(
                                                            {
                                                                "option{0}".format(k): sh.cell_value(i, j),
                                                                "score": sh.cell_value(i, j + 1),
                                                                "childquestionid": [
                                                                    Question.query.filter_by(name=child).first().id for
                                                                    child in
                                                                    sh.cell_value(i, j + 2).split(',') if
                                                                    Question.query.filter_by(name=child) is
                                                                    not None] if ',' in sh.cell_value(
                                                                    i, j + 2)
                                                                else 0 if Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)) is None else
                                                                Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)).first().id
                                                                if sh.cell_value(i, j + 2) != ''
                                                                else 0
                                                            })
                                                        maxscore = maxscore + int(sh.cell_value(i, j + 1))
                                                        k = k + 1
                                                    else:
                                                        break
                                            elif sh.cell_value(i, 8) == 'Single choice':
                                                k = 1
                                                scores = []
                                                for j in range(9, sh.ncols, 3):
                                                    if sh.cell_value(i, j) != '':
                                                        answers.append(
                                                            {
                                                                "option{0}".format(k): sh.cell_value(i, j),
                                                                "score": sh.cell_value(i, j + 1),
                                                                "childquestionid": [
                                                                    Question.query.filter_by(name=child).first().id for
                                                                    child in
                                                                    sh.cell_value(i, j + 2).split(',') if
                                                                    Question.query.filter_by(name=child) is
                                                                    not None] if ',' in sh.cell_value(
                                                                    i, j + 2)
                                                                else 0 if Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)) is None else
                                                                Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)).first().id
                                                                if sh.cell_value(i, j + 2) != ''
                                                                else 0
                                                            })
                                                        scores.append(int(sh.cell_value(i, j + 1)))
                                                        k = k + 1
                                                    else:
                                                        break
                                                    maxscore = max(scores)
                                            quesins = Question(sh.cell_value(i, 7), sh.cell_value(i, 8), answers,
                                                               maxscore,
                                                               subfuncins.id,
                                                               findfuncdata.id, findareadata.id, projins.id,
                                                               combination)
                                            db.session.add(quesins)
                                            db.session.commit()
                                        else:
                                            pass
                                    else:
                                        # add questions in sub func which already exists
                                        findsubfuncdata = Subfunctionality.query.filter(Subfunctionality.name ==
                                                                                        sh.cell_value(i, 4),
                                                                                        Subfunctionality.func_id ==
                                                                                        findfuncdata.id).one_or_none()
                                        combination = str(projins.id) + str(findareadata.id) + str(
                                            findfuncdata.id) + str(findsubfuncdata.id) + str(sh.cell_value(i, 7))
                                        existing_question = Question.query.filter(
                                            Question.combination == combination).one_or_none()
                                        if existing_question is None:
                                            maxscore = 0
                                            answers = []
                                            if sh.cell_value(i, 8) == 'Yes / No':
                                                answers = [
                                                    {
                                                        "option1": sh.cell_value(i, 9),
                                                        "score": sh.cell_value(i, 10),
                                                        "childquestionid": [
                                                            Question.query.filter_by(name=child).first().id for child in
                                                            sh.cell_value(i, 11).split(',') if Question.query.filter_by(
                                                                name=child) is not None] if ',' in sh.cell_value(i, 11)
                                                        else 0 if Question.query.filter_by(
                                                            name=sh.cell_value(i, 11)) is None else
                                                        Question.query.filter_by(name=sh.cell_value(i, 11)).first().id
                                                        if sh.cell_value(i, 11) != ''
                                                        else 0
                                                    },
                                                    {
                                                        "option2": sh.cell_value(i, 12),
                                                        "score": sh.cell_value(i, 13),
                                                        "childquestionid": [
                                                            Question.query.filter_by(name=child).first().id for child in
                                                            sh.cell_value(i, 14).split(',') if Question.query.filter_by(
                                                                name=child) is not None] if ',' in sh.cell_value(i, 14)
                                                        else 0 if Question.query.filter_by(
                                                            name=sh.cell_value(i, 14)) is None else
                                                        Question.query.filter_by(name=sh.cell_value(i, 14)).first().id
                                                        if sh.cell_value(i, 14) != ''
                                                        else 0
                                                    }
                                                ]
                                                maxscore = max(int(sh.cell_value(i, 10)), int(sh.cell_value(i, 13)))
                                            elif sh.cell_value(i, 8) == 'Multi choice':
                                                k = 1
                                                for j in range(9, sh.ncols, 3):
                                                    if sh.cell_value(i, j) != '':
                                                        answers.append(
                                                            {
                                                                "option{0}".format(k): sh.cell_value(i, j),
                                                                "score": sh.cell_value(i, j + 1),
                                                                "childquestionid": [
                                                                    Question.query.filter_by(name=child).first().id for
                                                                    child in
                                                                    sh.cell_value(i, j + 2).split(',') if
                                                                    Question.query.filter_by(name=child) is
                                                                    not None] if ',' in sh.cell_value(
                                                                    i, j + 2)
                                                                else 0 if Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)) is None else
                                                                Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)).first().id
                                                                if sh.cell_value(i, j + 2) != ''
                                                                else 0
                                                            })
                                                        maxscore = maxscore + int(sh.cell_value(i, j + 1))
                                                        k = k + 1
                                                    else:
                                                        break
                                            elif sh.cell_value(i, 8) == 'Single choice':
                                                k = 1
                                                scores = []
                                                for j in range(9, sh.ncols, 3):
                                                    if sh.cell_value(i, j) != '':
                                                        answers.append(
                                                            {
                                                                "option{0}".format(k): sh.cell_value(i, j),
                                                                "score": sh.cell_value(i, j + 1),
                                                                "childquestionid": [
                                                                    Question.query.filter_by(name=child).first().id for
                                                                    child in
                                                                    sh.cell_value(i, j + 2).split(',') if
                                                                    Question.query.filter_by(name=child) is
                                                                    not None] if ',' in sh.cell_value(
                                                                    i, j + 2)
                                                                else 0 if Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)) is None else
                                                                Question.query.filter_by(
                                                                    name=sh.cell_value(i, j + 2)).first().id
                                                                if sh.cell_value(i, j + 2) != ''
                                                                else 0
                                                            })
                                                        scores.append(int(sh.cell_value(i, j + 1)))
                                                        k = k + 1
                                                    else:
                                                        break
                                                    maxscore = max(scores)
                                            quesins = Question(sh.cell_value(i, 7), sh.cell_value(i, 8), answers,
                                                               maxscore,
                                                               findsubfuncdata.id,
                                                               findfuncdata.id, findareadata.id, projins.id,
                                                               combination)
                                            db.session.add(quesins)
                                            db.session.commit()
                                        else:
                                            pass
                                else:
                                    # add questions in func when subfunc does not exists for this func
                                    findfuncdata = Functionality.query.filter_by(
                                        name=sh.cell_value(i, 2),
                                        area_id=findareadata.id).first()
                                    combination = str(projins.id) + str(findareadata.id) + str(
                                        findfuncdata.id) + str(sh.cell_value(i, 7))
                                    existing_question = Question.query.filter(
                                        Question.combination == combination).one_or_none()
                                    if existing_question is None:
                                        maxscore = 0
                                        answers = []
                                        if sh.cell_value(i, 8) == 'Yes / No':
                                            answers = [
                                                {
                                                    "option1": sh.cell_value(i, 9),
                                                    "score": sh.cell_value(i, 10),
                                                    "childquestionid": [
                                                        Question.query.filter_by(name=child).first().id for child in
                                                        sh.cell_value(i, 11).split(',') if Question.query.filter_by(
                                                            name=child) is not None] if ',' in sh.cell_value(i, 11)
                                                    else 0 if Question.query.filter_by(
                                                        name=sh.cell_value(i, 11)) is None else
                                                    Question.query.filter_by(name=sh.cell_value(i, 11)).first().id
                                                    if sh.cell_value(i, 11) != ''
                                                    else 0
                                                },
                                                {
                                                    "option2": sh.cell_value(i, 12),
                                                    "score": sh.cell_value(i, 13),
                                                    "childquestionid": [
                                                        Question.query.filter_by(name=child).first().id for child in
                                                        sh.cell_value(i, 14).split(',') if Question.query.filter_by(
                                                            name=child) is not None] if ',' in sh.cell_value(i, 14)
                                                    else 0 if Question.query.filter_by(
                                                        name=sh.cell_value(i, 14)) is None else
                                                    Question.query.filter_by(name=sh.cell_value(i, 14)).first().id
                                                    if sh.cell_value(i, 14) != ''
                                                    else 0
                                                }
                                            ]
                                            maxscore = max(int(sh.cell_value(i, 10)), int(sh.cell_value(i, 13)))
                                        elif sh.cell_value(i, 8) == 'Multi choice':
                                            k = 1
                                            for j in range(9, sh.ncols, 3):
                                                if sh.cell_value(i, j) != '':
                                                    answers.append(
                                                        {
                                                            "option{0}".format(k): sh.cell_value(i, j),
                                                            "score": sh.cell_value(i, j + 1),
                                                            "childquestionid": [
                                                                Question.query.filter_by(name=child).first().id for
                                                                child in
                                                                sh.cell_value(i, j + 2).split(',') if
                                                                Question.query.filter_by(name=child) is
                                                                not None] if ',' in sh.cell_value(
                                                                i, j + 2)
                                                            else 0 if Question.query.filter_by(
                                                                name=sh.cell_value(i, j + 2)) is None else
                                                            Question.query.filter_by(
                                                                name=sh.cell_value(i, j + 2)).first().id
                                                            if sh.cell_value(i, j + 2) != ''
                                                            else 0
                                                        })
                                                    maxscore = maxscore + int(sh.cell_value(i, j + 1))
                                                    k = k + 1
                                                else:
                                                    break
                                        elif sh.cell_value(i, 8) == 'Single choice':
                                            k = 1
                                            scores = []
                                            for j in range(9, sh.ncols, 3):
                                                if sh.cell_value(i, j) != '':
                                                    answers.append(
                                                        {
                                                            "option{0}".format(k): sh.cell_value(i, j),
                                                            "score": sh.cell_value(i, j + 1),
                                                            "childquestionid": [
                                                                Question.query.filter_by(name=child).first().id for
                                                                child in
                                                                sh.cell_value(i, j + 2).split(',') if
                                                                Question.query.filter_by(name=child) is
                                                                not None] if ',' in sh.cell_value(
                                                                i, j + 2)
                                                            else 0 if Question.query.filter_by(
                                                                name=sh.cell_value(i, j + 2)) is None else
                                                            Question.query.filter_by(
                                                                name=sh.cell_value(i, j + 2)).first().id
                                                            if sh.cell_value(i, j + 2) != ''
                                                            else 0
                                                        })
                                                    scores.append(int(sh.cell_value(i, j + 1)))
                                                    k = k + 1
                                                else:
                                                    break
                                                maxscore = max(scores)
                                        quesins = Question(sh.cell_value(i, 7), sh.cell_value(i, 8), answers,
                                                           maxscore,
                                                           None,
                                                           findfuncdata.id, findareadata.id, projins.id,
                                                           combination)
                                        db.session.add(quesins)
                                        db.session.commit()
                                    else:
                                        pass
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
    """
        ---
        post:
          description: Fetch a project.
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
              - updatedeleteproject
        put:
          description: Update a project.
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
              - updatedeleteproject
        delete:
          description: Delete a project.
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
              - updatedeleteproject
    """
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
                        projdesc = res['ProjectDescription']
                        levels = res['Levels']
                        if 'NeedForReview' in res:
                            nfr = res['NeedForReview']
                        else:
                            nfr = 1
                        data.first().description = projdesc
                        data.first().levels = levels
                        data.first().needforreview = nfr
                        db.session.add(data.first())
                        db.session.commit()
                        return make_response(jsonify({"message": f"Project {data.first().name} "
                                                                 f"successfully updated."})), 200

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
