from flask import *
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
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
                                                      'userid': compuserdet.id})), 200
                    else:
                        return make_response(jsonify({"message": "Incorrect credentials !!"})), 401
                else:
                    return make_response(jsonify({"message": "User does not exist !!"})), 404
            else:
                return make_response(jsonify({"message": "Please provide email and password to login."})), 400
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400
