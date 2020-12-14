from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.rbac_model import Rbac
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

rbac = Blueprint('rbac', __name__)

colsrbac = ['id', 'feature', 'roles']


@rbac.route('/api/rbac', methods=['GET', 'POST'])
def rolebasedaccesscontrol():
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
            resp = Companyuserdetails.decode_auth_token(auth_token)
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
