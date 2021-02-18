from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.rbac_model import Role, Rbac
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

rbac = Blueprint('rbac', __name__)

colsrole = ['id', 'name', 'companyid', 'creationdatetime']
colsrbac = ['id', 'feature', 'url', 'icon', 'button', 'roles', 'creationdatetime', 'updationdatetime']


@rbac.route('/api/role', methods=['GET', 'POST'])
def rolemaster():
    """
        ---
        get:
          description: Fetch role(s).
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
              - getcreaterole
        post:
          description: Create a role.
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
              - getcreaterole
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
                    data = Role.query.all()
                    result = [{col: getattr(d, col) for col in colsrole} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    companyid = res['companyid']
                    role = res['name']
                    existing_role = Role.query.filter(Role.name == role, Role.companyid == companyid).one_or_none()
                    if existing_role is None:
                        roleins = Role(role, companyid)
                        db.session.add(roleins)
                        db.session.commit()
                        data = Role.query.filter_by(id=roleins.id)
                        result = [{col: getattr(d, col) for col in colsrole} for d in data]
                        return make_response(jsonify({"message": f"Role {role} successfully inserted.",
                                                      "data": result[0]})), 201
                    else:
                        return make_response(jsonify({"message": f"Role {role} already exists."})), 400
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@rbac.route('/api/updelrole/', methods=['DELETE'])
def updelrolemaster():
    """
        ---
        delete:
          description: Delete a role.
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
              - deleterole
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
                roleid = res['roleid']
                data = Role.query.filter_by(id=roleid)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'DELETE':
                        allrbacdata = Rbac.query.all()
                        for d in allrbacdata:
                            rbacdata = Rbac.query.filter_by(id=d.id).first()
                            if data.first().name != rbacdata.roles:
                                if data.first().name in str(rbacdata.roles).split(','):
                                    rbacdata.roles = ','.join(
                                        [s for s in str(rbacdata.roles).split(',') if s != data.first().name])
                                    db.session.add(rbacdata)
                                    db.session.commit()
                                else:
                                    pass
                            else:
                                db.session.delete(rbacdata)
                                db.session.commit()
                        userdata = Companyuserdetails.query.filter_by(emprole=data.first().name)
                        for u in userdata:
                            u.emprole = 'no role'
                            db.session.add(u)
                            db.session.commit()
                        db.session.delete(data.first())
                        db.session.commit()
                        return make_response(jsonify({"message": f"Role with ID {roleid} "
                                                                 f"successfully deleted."})), 204
            else:
                return make_response(({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@rbac.route('/api/rbac', methods=['GET', 'POST'])
def rolebasedaccesscontrol():
    """
        ---
        get:
          description: Fetch RBAC(s).
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
              - getcreaterbac
        post:
          description: Create a RBAC.
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
              - getcreaterbac
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
                    data = Rbac.query.all()
                    result = [{col: getattr(d, col) for col in colsrbac} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    feat = res['feature']
                    existing_feature = Rbac.query.filter(Rbac.feature == feat).one_or_none()
                    if existing_feature is None:
                        featins = Rbac(feat, res['url'], res['icon'], res['button'], res['roles'])
                        db.session.add(featins)
                        db.session.commit()
                        data = Rbac.query.filter_by(id=featins.id)
                        result = [{col: getattr(d, col) for col in colsrbac} for d in data]
                        return make_response(jsonify({"message": f"RBAC with Feature {feat} "
                                                                 f"successfully inserted.",
                                                      "data": result[0]})), 201
                    else:
                        return make_response(jsonify({"message": f"RBAC with Feature {feat} already exists."})), 400
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@rbac.route('/api/updelrbac/', methods=['POST', 'PUT'])
def updelrolebasedaccesscontrol():
    """
        ---
        post:
          description: Fetch a RBAC.
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
              - updatedeleterbac
        put:
          description: Update a RBAC.
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
              - updatedeleterbac
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
                rbacid = res['rbacid']
                data = Rbac.query.filter_by(id=rbacid)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'POST':
                        result = [{col: getattr(d, col) for col in colsrbac} for d in data]
                        return make_response(jsonify({"data": result[0]})), 200
                    elif request.method == 'PUT':
                        data.first().url = res['url']
                        data.first().icon = res['icon']
                        data.first().button = res['button']
                        data.first().roles = res['Roles']
                        db.session.add(data.first())
                        db.session.commit()
                        return make_response(jsonify({"message": f"RBAC with Feature {data.first().feature} "
                                                                 f"successfully updated."})), 200
            else:
                return make_response(({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@rbac.route('/api/fetchfeaturesbyrole/', methods=['POST'])
def fetchfeaturesbyrole():
    """
        ---
        post:
          description: Fetch features by role.
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
              - fetchfeaturesbyrole
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
                result = []
                role = res['role']
                if request.method == 'POST':
                    allrbacdata = Rbac.query.all()
                    for d in allrbacdata:
                        rbacdata = Rbac.query.filter_by(id=d.id).first()
                        if role in str(rbacdata.roles).split(','):
                            result.append({"feature": rbacdata.feature, "url": rbacdata.url, "icon": rbacdata.icon,
                                           "button": rbacdata.button})
                        else:
                            pass
                    return make_response(jsonify({"Features details": result})), 200
            else:
                return make_response(({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
