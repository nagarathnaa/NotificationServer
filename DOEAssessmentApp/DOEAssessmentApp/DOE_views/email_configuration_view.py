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
                    return jsonify({"data": result})
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    mailid = res['Email']
                    host = res['Host']
                    existing_email = Emailconfiguration.query.filter(Emailconfiguration.email == mailid).one_or_none()
                    if existing_email is None:
                        emailconf = Emailconfiguration(mailid, host, generate_password_hash(res['Password']))
                        db.session.add(emailconf)
                        db.session.commit()
                        return jsonify(
                            {"message": f"Email Configuration with Email ID {mailid} successfully inserted."})
                    else:
                        return jsonify({"message": f"Email Configuration with Email ID {mailid} already exists."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e


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
                data = Emailconfiguration.query.filter_by(id=emailconfid).first()
                if data is None:
                    return jsonify({"message": "Incorrect ID"})
                else:
                    if request.method == 'GET':
                        result = [{col: getattr(d, col) for col in colsemailconf} for d in data]
                        return jsonify({"data": result[0]})
                    elif request.method == 'PUT':
                        data.email = res['Email']
                        data.host = res['Host']
                        data.password = generate_password_hash(res['Password'])
                        db.session.add(data)
                        db.session.commit()
                        return jsonify(
                            {"message": f"Email Configuration with Email ID {res['Email']} successfully updated."})
                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        return jsonify({"message": f"Email Configuration with ID {emailconfid} successfully deleted."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e
