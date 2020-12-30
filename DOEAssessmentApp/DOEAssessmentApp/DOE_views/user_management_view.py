from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

user_management_view = Blueprint('user_management_view', __name__)

colsusermanagement = ['id', 'empid', 'empname', 'emprole', 'empemail', 'emppasswordhash', 'companyid',
                      'creationdatetime', 'updationdatetime']


@user_management_view.route('/api/usermanagement', methods=['GET', 'POST'])
def getAndPost():
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
                    data = Companyuserdetails.query.all()
                    result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    user_name = res['empname']
                    usermanagement = Companyuserdetails(res['empid'], res['empname'], res['emprole'], res['empemail'],
                                                        res['emppasswordhash'], res['companyid'])
                    db.session.add(usermanagement)
                    db.session.commit()
                    data = Companyuserdetails.query.filter_by(id=usermanagement.id)
                    result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                    return make_response(jsonify({"msg": f"UserManagement {user_name} successfully inserted.",
                                                  "data": result[0]})), 201
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@user_management_view.route('/api/updelusermanagement/', methods=['GET', 'PUT', 'DELETE'])
def updateAndDelete():
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
                row_id = res['row_id']
                data = Companyuserdetails.query.filter_by(id=row_id)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'GET':
                        result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
                        return make_response(jsonify({"data": result[0]})), 200
                    elif request.method == 'PUT':
                        user_name = res['empname']
                        user_emppasswordhash = res['emppasswordhash']
                        data.first().emppasswordhash = user_emppasswordhash
                        data.first().empname = user_name
                        db.session.add(data.first())
                        db.session.commit()
                        return make_response(jsonify({"msg": f"UserManagement {user_name} successfully updated."})), 200
                    elif request.method == 'DELETE':
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
