from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.email_configuration_model import Emailconfiguration
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from werkzeug.security import generate_password_hash

emailconfig = Blueprint('emailconfig', __name__)

colsemailconf = ['id', 'email', 'host', 'passwordhash', 'creationdatetime', 'updationdatetime']


@emailconfig.route('/api/emailconfig', methods=['GET', 'POST'])
def emailconfigs():
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
                    data = Emailconfiguration.query.all()
                    result = [{col: getattr(d, col) for col in colsemailconf} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    mailid = res['Email']
                    host = res['Host']
                    existing_email = Emailconfiguration.query.filter(Emailconfiguration.email == mailid).one_or_none()
                    if existing_email is None:
                        emailconf = Emailconfiguration(mailid, host, generate_password_hash(res['Password']))
                        db.session.add(emailconf)
                        db.session.commit()
                        return make_response(jsonify({"message": f"Email Configuration with Email ID {mailid} "
                                                                 f"successfully inserted."})), 201
                    else:
                        return make_response(jsonify({"message": f"Email Configuration with Email ID {mailid} "
                                                                 f"already exists."})), 400
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@emailconfig.route('/api/updelemailconfig/', methods=['GET', 'PUT', 'DELETE'])
def updelemailconfig():
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
                emailconfid = res['emailconfid']
                data = Emailconfiguration.query.filter_by(id=emailconfid)
                if data is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'GET':
                        result = [{col: getattr(d, col) for col in colsemailconf} for d in data]
                        return make_response(jsonify({"data": result[0]})), 200
                    elif request.method == 'PUT':
                        data.first().email = res['Email']
                        data.first().host = res['Host']
                        data.first().password = generate_password_hash(res['Password'])
                        db.session.add(data.first())
                        db.session.commit()
                        return make_response(jsonify({"message": f"Email Configuration with Email ID {res['Email']} "
                                                                 f"successfully updated."})), 200
                    elif request.method == 'DELETE':
                        db.session.delete(data.first())
                        db.session.commit()
                        return make_response(jsonify({"message": f"Email Configuration with ID {emailconfid} "
                                                                 f"successfully deleted."})), 204
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400
