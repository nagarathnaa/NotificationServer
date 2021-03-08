from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.tools_login_model import ToolsLogin

from werkzeug.security import generate_password_hash

loginconfig = Blueprint('loginconfig', __name__)

colsloginconf = ['id', 'name', 'url', 'password', 'projectid', 'creationdatetime', 'updationdatetime']


@loginconfig.route('/api/toolslogin', methods=['GET', 'POST'])
def toolslogin():
    try:
        if request.method == "GET":
            data = ToolsLogin.query.all()
            result = [{col: getattr(d, col) for col in colsloginconf} for d in data]
            return jsonify({"data": result})
        elif request.method == "POST":
            res = request.get_json(force=True)
            name = res['name']
            url = res['url']
            projectid = res['projectid']
            existing_name = ToolsLogin.query.filter(ToolsLogin.name == name).one_or_none()
            if existing_name is None:
                login_conf = ToolsLogin(name, url, generate_password_hash(res['password']), projectid)
                db.session.add(login_conf)
                db.session.commit()
                return jsonify(
                    {"message": f"Tools Configuration with tool name {name} successfully inserted."}), 201
            else:
                return jsonify({"message": f"Tools Configuration with tool name {name} already exists."}), 400
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@loginconfig.route('/api/updellogin/', methods=['GET', 'PUT', 'DELETE'])
def updellogin():
    try:
        res = request.get_json(force=True)
        nameid = res['nameid']
        data = ToolsLogin.query.filter_by(id=nameid).first()
        if data is None:
            return jsonify({"message": "Incorrect ID"})
        else:
            if request.method == 'GET':
                result = [{col: getattr(d, col) for col in colsloginconf} for d in data]
                return jsonify({"data": result[0]})
            elif request.method == 'PUT':
                data.name = res['name']
                data.url = res['url']
                data.password = generate_password_hash(res['password'])
                db.session.add(data)
                db.session.commit()
                return jsonify(
                    {"message": f"Tools Configuration with tool ID {res['name']} successfully updated."}), 200
            elif request.method == 'DELETE':
                db.session.delete(data)
                db.session.commit()
                return jsonify({"message": f"Tools Configuration with tool ID {nameid} successfully deleted."}), 204
    except Exception as e:
        return e
