"""
Routes and views for DOEAssesmentApp.
"""

import uuid
from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.models import Emailconfiguration, Rbac, Companydetails, Companyadmindetails
from werkzeug.security import generate_password_hash, check_password_hash

emailconfig = Blueprint('emailconfig', __name__)
rbac = Blueprint('rbac', __name__)
companydetails = Blueprint('companydetails', __name__)
companyadmindetails = Blueprint('companyadmindetails', __name__)

colsemailconf = ['id', 'email', 'host', 'passwordhash']
colsrbac = ['id', 'feature', 'roles']
colscompanydetails = ['id', 'companyname', 'registeredaddress', 'billingaddress', 'gstortaxnumber', 'registrationkey', 'registrationkeyvalidated', 'creationdatetime']
colscompanyadmindetails = ['id', 'adminname', 'adminemail', 'adminpasswordhash', 'companyid', 'creationdatetime']

@emailconfig.route('/api/emailconfig', methods=['GET', 'POST'])
def emailconfigs():
    try:
       auth_header = request.headers.get('Authorization')
       if auth_header:
           auth_token = auth_header.split(" ")[1]
       else:
           auth_token = ''
       if auth_token:
           resp = Companyadmindetails.decode_auth_token(auth_token)
           if isinstance(resp, str):
               if request.method == "GET":
                   data = Emailconfiguration.query.all()
                   result = [{col: getattr(d, col) for col in colsemailconf} for d in data]
                   return jsonify(result)
               elif request.method == "POST":
                   res = request.get_json(force=True)
                   mailid = res['Email']
                   host = res['Host']
                   existing_email = Emailconfiguration.query.filter(Emailconfiguration.email == mailid).one_or_none()
                   if existing_email is None:
                       emailconf = Emailconfiguration(mailid, host, generate_password_hash(res['Password']))
                       db.session.add(emailconf)
                       db.session.commit()
                       return jsonify({"message": f"Email Configuration with Email ID {mailid} successfully inserted."})
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
           resp = Companyadmindetails.decode_auth_token(auth_token)
           if isinstance(resp, str):
               res = request.get_json(force=True)
               emailconfid = res['emailconfid']
               data = Emailconfiguration.query.filter_by(id=emailconfid).first()
               if data is None:
                   return jsonify({"message": "Incorrect ID"})
               else:
#                  if request.method == 'GET':
#                      result = [{col: getattr(d, col) for col in colsemailconf} for d in data]
#                      return jsonify(result)
                   if request.method == 'PUT':
                       data.email = res['Email']
                       data.host = res['Host']
                       data.password = generate_password_hash(res['Password'])
                       db.session.add(data)
                       db.session.commit()
                       return jsonify({"message": f"Email Configuration with Email ID {res['Email']} successfully updated."})
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

@emailconfig.route("/hello")
def hello():
     return 'Hello Srijib!'

@rbac.route('/api/rbac', methods=['GET', 'POST'])
def rolebasedaccesscontrol():
    try:
       auth_header = request.headers.get('Authorization')
       if auth_header:
           auth_token = auth_header.split(" ")[1]
       else:
           auth_token = ''
       if auth_token:
           resp = Companyadmindetails.decode_auth_token(auth_token)
           if isinstance(resp, str):
               if request.method == "GET":
                   data = Rbac.query.all()
                   result = [{col: getattr(d, col) for col in colsrbac} for d in data]
                   return jsonify(result)
               elif request.method == "POST":
                   res = request.get_json(force=True)
                   feat = res['Feature']
                   existing_feature = Rbac.query.filter(Rbac.feature == feat).one_or_none()
                   if existing_feature is None:
                       featins = Rbac(feat, res['Roles'])
                       db.session.add(featins)
                       db.session.commit()
                       return jsonify({"message": f"RBAC with Feature {feat} successfully inserted."})
                   else:
                       return jsonify({"message": f"RBAC with Feature {feat} already exists."})
           else:
               return jsonify({"message": resp})
       else:
           return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e

@rbac.route('/api/updelrbac/', methods=['GET', 'PUT', 'DELETE'])
def updelrolebasedaccesscontrol():
    try:
       auth_header = request.headers.get('Authorization')
       if auth_header:
           auth_token = auth_header.split(" ")[1]
       else:
           auth_token = ''
       if auth_token:
           resp = Companyadmindetails.decode_auth_token(auth_token)
           if isinstance(resp, str):
               res = request.get_json(force=True)
               rbacid = res['rbacid']
               data = Rbac.query.filter_by(id=rbacid).first()
               if data is None:
                   return jsonify({"message": "Incorrect ID"})
               else:
#                  if request.method == 'GET':
#                      result = [{col: getattr(d, col) for col in colsrbac} for d in data]
#                      return jsonify(result)
                   if request.method == 'PUT':
                       data.feature = res['Feature']
                       data.roles = res['Roles']
                       db.session.add(data)
                       db.session.commit()
                       return jsonify({"message": f"RBAC with Feature {res['Feature']} successfully updated."})
                   elif request.method == 'DELETE':
                       db.session.delete(data)
                       db.session.commit()
                       return jsonify({"message": f"RBAC with ID {rbacid} successfully deleted."})
           else:
               return jsonify({"message": resp})
       else:
           return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e

@companydetails.route('/api/companydetails', methods=['GET', 'POST'])
def companydetail():
    try:
       if request.method == "GET":
           data = Companydetails.query.all()
           result = [{col: getattr(d, col) for col in colscompanydetails} for d in data]
           return jsonify(result)
       elif request.method == "POST":
           res = request.get_json(force=True)
           cname = res['CompanyName']
           regadrs = res['RegisteredAddress']
           billadrs = res['BillingAddress']
           gstno = res['GstorTaxNumber']
           admname = res['AdminName']
           admemail = res['AdminEmail']
           regkey = str(uuid.uuid4())
           existing_company = Companydetails.query.filter(Companydetails.companyname == cname).one_or_none()
           if existing_company is None:
               compdet = Companydetails(cname, regadrs, billadrs, gstno, regkey)
               db.session.add(compdet)
               db.session.commit()
               compadmindet = Companyadmindetails(admname, admemail, generate_password_hash(res['AdminPassword']), compdet.id)
               db.session.add(compadmindet)
               db.session.commit()
               return jsonify({"message": f"Company details with Company Name {cname} successfully inserted."})
           else:
               return jsonify({"message": f"Company details with Company Name {cname} already exists."})
    except Exception as e:
        return e

@companydetails.route('/api/login', methods=['POST'])
def login():
    try:
       if request.method == "POST":
           res = request.get_json(force=True)
           if res and 'Email' in res and 'Password' in res:
               compadmdet = Companyadmindetails.query.filter_by(adminemail = res['Email']).first()
               if compadmdet:
                   if check_password_hash(compadmdet.adminpasswordhash, res['Password']):
                       token = compadmdet.encode_auth_token(res['Email'])
                       return jsonify({'token' : token.decode('UTF-8')})
                   else:
                       return jsonify({"message": "Incorrect credentials !!"})
               else:
                   return jsonify({"message": "User does not exist !!"})
           else:
               return jsonify({"message": "Please provide email and password to login."})
    except Exception as e:
        return e
