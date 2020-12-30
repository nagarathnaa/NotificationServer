from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_assignment_to_manager_model import Projectassignmenttomanager
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

assigningprojectmanager = Blueprint('assigningprojectmanager', __name__)


@assigningprojectmanager.route('/api/assigningprojectmanager', methods=['GET', 'POST'])
def getAndPost():
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
                    results = []
                    data = Projectassignmenttomanager.query.all()
                    for user in data:
                        json_data = {'id': user.id, 'emp_id': user.emp_id, 'project_id': user.project_id,
                                     'status': user.status, 'creationdatetime': user.creationdatetime,
                                     'updationdatetime': user.updationdatetime}
                        results.append(json_data)
                    return make_response(jsonify({"data": results})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    pm_id = res['emp_id']
                    pm_project_id = res['project_id']
                    existing_projectmanager = Projectassignmenttomanager.query.filter(Projectassignmenttomanager.emp_id
                                                                                      == pm_id,
                                                                                      Projectassignmenttomanager.
                                                                                      project_id
                                                                                      == pm_project_id).one_or_none()
                    if existing_projectmanager is None:
                        project_managers_in = Projectassignmenttomanager(pm_id, pm_project_id)
                        db.session.add(project_managers_in)
                        db.session.commit()
                        return make_response(jsonify({"msg": "project manager successfully assigned."})), 201
                    else:
                        return make_response(jsonify({"msg": f"project manager was already assigned before."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningprojectmanager.route('/api/associateprojectmanager/', methods=['PUT'])
def updateAndDelete():
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
                row_id = res['row_id']
                data = Projectassignmenttomanager.query.filter_by(id=row_id).first()
                if data is None:
                    return make_response(jsonify({"msg": "Incorrect ID"})), 404
                else:
                    if request.method == 'PUT':
                        associate_status = res['associate_status']
                        if associate_status == 1:
                            data.status = 1
                            db.session.add(data)
                            db.session.commit()
                            return make_response(jsonify({"msg": "project manager associated successfully "})), 200
                        else:
                            data.status = 0
                            db.session.add(data)
                            db.session.commit()
                            return make_response(jsonify({"msg": "project manager disassociated successfully"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
