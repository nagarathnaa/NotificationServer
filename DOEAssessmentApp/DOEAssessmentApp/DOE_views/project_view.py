from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

proj = Blueprint('proj', __name__)

colsproject = ['id', 'name', 'description', 'companyid', 'creationdatetime', 'updationdatetime']


@proj.route('/api/project', methods=['GET', 'POST'])
def project():
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
                    return jsonify({"data": result})
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    projname = res['ProjectName']
                    projdesc = res['ProjectDescription']
                    comp_id = res['CompanyID']
                    existing_project = Project.query.filter(Project.name == projname,
                                                            Project.companyid == comp_id).one_or_none()
                    if existing_project is None:
                        projins = Project(projname, projdesc, comp_id)
                        db.session.add(projins)
                        db.session.commit()
                        return jsonify({"message": f"Project {projname} successfully inserted."})
                    else:
                        return jsonify({"message": f"Project {projname} already exists for the company {comp_id}."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e


@proj.route('/api/updelproject/', methods=['GET', 'PUT', 'DELETE'])
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
                data = Project.query.filter_by(id=projid).first()
                if data is None:
                    return jsonify({"message": "Incorrect ID"})
                else:
                    if request.method == 'GET':
                        result = [{col: getattr(d, col) for col in colsproject} for d in data]
                        return jsonify({"data": result[0]})
                    elif request.method == 'PUT':
                        projectname = res['ProjectName']
                        compid = res['CompanyID']
                        existing_project = Project.query.filter(Project.name == projectname,
                                                             Project.companyid == compid).one_or_none()
                        if existing_project is None:
                            data.name = projectname
                            db.session.add(data)
                            db.session.commit()
                            return jsonify({"message": f"Project {projectname} successfully updated."})
                        else:
                            return jsonify({"message": f"Project {projectname} already exists for the company {compid}."})
                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        return jsonify({"message": f"Project with ID {projid} successfully deleted."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e
