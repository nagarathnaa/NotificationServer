from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.project_assignment_to_manager_model import Projectassignmenttomanager
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

assigningprojectmanager = Blueprint('assigningprojectmanager', __name__)


@assigningprojectmanager.route('/api/assigningprojectmanager', methods=['GET', 'POST'])
def getandpost():
    """
        ---
        get:
          description: Fetch project manager(s) assigned to project(s).
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
              - getcreateprojectmanagerassignment
        post:
          description: Assign a project to a project manager.
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
              - getcreateprojectmanagerassignment
    """
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    results = []
                    data = Projectassignmenttomanager.query.all()
                    for user in data:
                        userdata = Companyuserdetails.query.filter_by(empid=user.emp_id)
                        data_proj = Project.query.filter_by(id=user.project_id)
                        if userdata.first() is not None and data_proj.first() is not None:
                            json_data = {'id': user.id, 'emp_id': user.emp_id, 'emp_name': userdata.first().empname,
                                         'project_id': user.project_id, 'project_name': data_proj.first().name,
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
                        data = Projectassignmenttomanager.query.filter_by(id=project_managers_in.id).first()
                        userdata = Companyuserdetails.query.filter_by(empid=data.emp_id).first()
                        data_proj = Project.query.filter_by(id=data.project_id).first()
                        result = {'id': data.id, 'emp_id': data.emp_id, 'emp_name': userdata.empname,
                                  'project_id': data.project_id, 'project_name': data_proj.name,
                                  'status': data.status, 'creationdatetime': data.creationdatetime,
                                  'updationdatetime': data.updationdatetime}
                        return make_response(jsonify({"msg": "project manager successfully assigned.",
                                                      "data": result})), 201
                    else:
                        return make_response(jsonify({"msg": "project manager was already assigned before."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningprojectmanager.route('/api/associateprojectmanager/', methods=['PUT'])
def updateanddelete():
    """
        ---
        put:
          description: Associate/Disassociate a project manager.
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
              - associateprojectmanager
    """
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
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


@assigningprojectmanager.route('/api/fetchprojectsassignedtomanager/', methods=['POST'])
def fetchprojectsassignedtomanager():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if 'empid' in session and Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    results = []
                    res = request.get_json(force=True)
                    empid = res['emp_id']
                    data = Projectassignmenttomanager.query.filter_by(emp_id=empid)
                    for d in data:
                        data_proj = Project.query.filter_by(id=d.project_id)
                        if data_proj.first() is not None:
                            json_data = {'id': d.project_id, 'name': data_proj.first().name,
                                         'status': d.status, 'creationdatetime': d.creationdatetime,
                                         'updationdatetime': d.updationdatetime}
                            results.append(json_data)
                    return make_response(jsonify({"data": results})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
