from flask import *
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from werkzeug.security import check_password_hash

companyuserdetails = Blueprint('companyuserdetails', __name__)

colscompanyuserdetails = ['id', 'empid', 'empname', 'emprole', 'empemail', 'emppasswordhash', 'companyid',
                          'creationdatetime']


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
                        return jsonify(
                            {'token': token.decode('UTF-8'), 'type': compuserdet.emprole, 'userid': compuserdet.id})
                    else:
                        return jsonify({"message": "Incorrect credentials !!"})
                else:
                    return jsonify({"message": "User does not exist !!"})
            else:
                return jsonify({"message": "Please provide email and password to login."})
    except Exception as e:
        return e
