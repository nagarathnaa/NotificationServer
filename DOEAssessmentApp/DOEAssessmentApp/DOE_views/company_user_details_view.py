from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails, BlacklistToken
from werkzeug.security import check_password_hash

companyuserdetails = Blueprint('companyuserdetails', __name__)

colscompanyuserdetails = ['id', 'empid', 'empname', 'emprole', 'empemail', 'emppasswordhash', 'companyid',
                          'creationdatetime', 'updationdatetime']


@companyuserdetails.route('/api/login', methods=['POST'])
def login():
    try:
        if request.method == "POST":
            res = request.get_json(force=True)
            if res and 'Email' in res and 'Password' in res:
                compuserdet = Companyuserdetails.query.filter_by(empemail=res['Email']).first()
                if compuserdet:
                    if check_password_hash(compuserdet.emppasswordhash, res['Password']):
                        token = compuserdet.encode_auth_token(res['Email'])
                        return make_response(jsonify({'token': token, 'type': compuserdet.emprole,
                                                      'emp_id': compuserdet.empid})), 200
                    else:
                        return make_response(jsonify({"message": "Incorrect credentials !!"})), 401
                else:
                    return make_response(jsonify({"message": "User does not exist !!"})), 404
            else:
                return make_response(jsonify({"message": "Please provide email and password to login."})), 400
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@companyuserdetails.route('/api/logout', methods=['POST'])
def logout():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                return make_response(jsonify({"message": "Successfully logged out."})), 200
            else:
                return make_response(({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 403
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
