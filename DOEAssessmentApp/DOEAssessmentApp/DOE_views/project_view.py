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
            if isinstance(resp, str):
                if request.method == "GET":
                    data = Project.query.all()
                    result = [{col: getattr(d, col) for col in colsproject} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
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
                        return make_response(jsonify({"message": f"Project {projname} successfully inserted."})), 201
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


@project.route('/api/updelproject/', methods=['GET', 'PUT', 'DELETE'])
def updelproject():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
                res = request.get_json(force=True)
                projid = res['projectid']
                data = Project.query.filter_by(id=projid)
                print(data, flush=True)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'GET':
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


