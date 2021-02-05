from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from werkzeug.security import generate_password_hash

user_management_view = Blueprint('user_management_view', __name__)

colsusermanagement = ['id', 'empid', 'empname', 'emprole', 'empemail', 'emppasswordhash', 'companyid',
                      'creationdatetime', 'updationdatetime']


@user_management_view.route('/api/usermanagement', methods=['GET', 'POST'])
def getAndPost():
    """
        ---
        get:
          description: Fetch user(s) details.
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
              - getcreateuser
        post:
          description: Create an user.
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
              - getcreateuser
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
                    data = Companyuserdetails.query.all()
                    result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    user_empid = res['empid']
                    user_name = res['empname']
                    user_role = res['emprole']
                    user_email = res['empemail']
                    user_companyid = res['companyid']
                    existing_user = Companyuserdetails.query.filter_by(empid=user_empid).one_or_none()
                    if existing_user is None:
                        usermanagement = Companyuserdetails(user_empid, user_name, user_role, user_email,
                                                            generate_password_hash(res['EmployeePassword']),
                                                            user_companyid)
                        db.session.add(usermanagement)
                        db.session.commit()
                        data = Companyuserdetails.query.filter_by(id=usermanagement.id)
                        result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                        return make_response(jsonify({"msg": f"UserManagement {user_name} successfully inserted.",
                                                      "data": result[0]})), 201
                    else:
                        return make_response(jsonify({"msg": f"UserManagement  {user_name} "
                                                             f"already exists."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@user_management_view.route('/api/updelusermanagement/', methods=['POST', 'PUT', 'DELETE'])
def updateAndDelete():
    """
        ---
        post:
          description: Fetch an user.
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
              - updatedeleteuser
        put:
          description: Update an user.
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
              - updatedeleteuser
        delete:
          description: Delete an user.
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
              - updatedeleteuser
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
                row_id = res['row_id']
                data = Companyuserdetails.query.filter_by(id=row_id)
                if data.first() is None:
                    return make_response(jsonify({"msg": "Incorrect ID"})), 404
                else:
                    if request.method == 'POST':
                        result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                        return make_response(jsonify({"data": result[0]})), 200
                    elif request.method == 'PUT':
                        res = request.get_json(force=True)
                        user_role = res['emprole']
                        if data.first().emprole == 'admin':
                            count_user_with_admin_role = Companyuserdetails.query.filter_by(emprole=user_role).count()
                            if count_user_with_admin_role > 1:
                                data.first().emprole = user_role
                                db.session.add(data.first())
                                db.session.commit()
                                return make_response(
                                    jsonify(
                                        {"msg": f"UserManagement successfully updated with role {user_role}."})), 200
                            else:
                                return make_response(
                                    jsonify({
                                        "msg": "Please assign a user to admin role before changing the current admin's role"})), 200
                        else:
                            data.first().emprole = user_role
                            db.session.add(data.first())
                            db.session.commit()
                            return make_response(
                                jsonify(
                                    {"msg": f"UserManagement successfully updated with role {user_role}."})), 200

                    elif request.method == 'DELETE':
                        res = request.get_json(force=True)
                        user_role = res['emprole']
                        if data.first().emprole == 'admin':
                            count_user_with_admin_role = Companyuserdetails.query.filter_by(emprole=user_role).count()
                            if count_user_with_admin_role > 1:
                                data.first().emprole = user_role
                                db.session.delete(data.first())
                                db.session.commit()
                                return make_response(
                                    jsonify(
                                        {"msg": f"UserManagement with ID {row_id} "
                                                f"successfully deleted."})), 204
                            else:
                                return make_response(jsonify({
                                    "msg": "Please assign a user to admin role before deleting the current admin's role."})), 204
                        else:
                            db.session.delete(data.first())
                            db.session.commit()
                            return make_response(jsonify({"msg": f"UserManagement with ID {row_id} "
                                                                 f"successfully deleted."})), 204
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@user_management_view.route('/api/fetchusersbyrole', methods=['POST'])
def fetchusersbyrole():
    """
        ---
        post:
          description: Fetch users by role.
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
              - fetchusersbyrole
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
                if request.method == "POST":
                    res = request.get_json(force=True)
                    user_role = res['emprole']
                    data = Companyuserdetails.query.filter_by(emprole=user_role)
                    if data.first() is not None:
                        result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                        return make_response(jsonify({"data": result})), 200
                    else:
                        return make_response(jsonify({"msg": f"No users present with {user_role} role."})), 404
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
