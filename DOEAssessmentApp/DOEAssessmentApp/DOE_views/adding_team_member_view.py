from flask import *
from __init__ import app, db
from DOE_models.adding_team_member_model import AddingTeamMember

adding_team_member_view = Blueprint('adding_team_member_view', __name__)

colsaddteam = ['emp_code', 'enter_team_member_name', 'project_name', 'area_name', 'roll', 'email_id',
               'functionality_name', 'subfunctionality_name']


@adding_team_member_view.route('/api/addingteammember', methods=['GET', 'POST'])
def getAndPost():
    try:
        if request.method == "GET":
            data = AddingTeamMember.query.all()
            result = [{col: getattr(d, col) for col in colsaddteam} for d in data]
            return make_response(jsonify(result)), 200
        elif request.method == "POST":
            res = request.get_json(force=True)
            addingteammember = AddingTeamMember(res['emp_code'], res['enter_team_member_name'], res['project_name'],
                                              res['area_name'], res['roll'], res['email_id'], res['functionality_name'],
                                              res['subfunctionality_name'])
            db.session.add(addingteammember)
            db.session.commit()
            return make_response(
                jsonify({"msg": "AddingTeamMember successfully inserted."})), 201

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@adding_team_member_view.route('/api/addingteammember/<emp_code>', methods=['PUT', 'DELETE'])
def updateAndDelete(emp_code):
    try:
        # data = AddingTeamMember.query.filter_by(emp_code=str(emp_code)).first()
        if request.method == "DELETE":
            db.session.query(AddingTeamMember).filter(AddingTeamMember.emp_code == emp_code).delete()
            # db.session.delete(data)
            db.session.commit()
            return make_response(
                jsonify({"msg": "AddingTeamMember with ID successfully deleted."})), 200
        elif request.method == "PUT":
            res = request.get_json(force=True)
            print(res)
            updateData = {}
            keys = res.keys()
            if "emp_code" in keys:
                updateData[AddingTeamMember.emp_code] = res["emp_code"]
            if "enter_team_member_name" in keys:
                updateData[AddingTeamMember.name] = res["enter_team_member_name"]
            if "project_name" in keys:
                updateData[AddingTeamMember.roll] = res["project_name"]
            if "area_name" in keys:
                updateData[AddingTeamMember.email] = res["area_name"]
            if "roll" in keys:
                updateData[AddingTeamMember.email] = res["roll"]
            if "email_id" in keys:
                updateData[AddingTeamMember.email] = res["email_id"]
            if "functionality_name" in keys:
                updateData[AddingTeamMember.email] = res["functionality_name"]
            if "subfunctionality_name" in keys:
                updateData[AddingTeamMember.email] = res["subfunctionality_name"]

            is_updated = db.session.query(AddingTeamMember).filter(AddingTeamMember.emp_code == emp_code).update(
                updateData)
            db.session.commit()
            if is_updated:
                return make_response({"msg": "emp_code: " + emp_code + " successfully updated"}), 200
            else:
                return make_response({"msg": "emp_code: " + emp_code + " unable to update"}), 401

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401
