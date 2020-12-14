from flask import *
from __init__ import app, db
from DOE_models.user_management_model import UserManagement

user_management_view = Blueprint('user_management_view', __name__)

colsusermanagement = ['emp_id', 'name', 'roll', 'email']


@user_management_view.route('/api/usermanagement', methods=['GET', 'POST'])
def getAndPost():
    try:
        if request.method == "GET":
            data = UserManagement.query.all()
            result = [{col: getattr(d, col) for col in colsusermanagement} for d in data]
            return make_response(jsonify(result)), 200
        elif request.method == "POST":
            res = request.get_json(force=True)
            # feat = res['Feature']
            # existing_feature = Rbac.query.filter(Rbac.feature == feat).one_or_none()
            # if existing_feature is None:
            usermanagement = UserManagement(res['emp_id'], res['name'], res['roll'], res['email'])
            db.session.add(usermanagement)
            db.session.commit()
            return make_response(
                jsonify({"msg": "UserManagement successfully inserted."})), 201
        # else:
        #     return make_response(jsonify({"message": f"UserManagement {usermanagement} already exists."})), 200
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@user_management_view.route('/api/usermanagement/<emp_id>', methods=['PUT', 'DELETE'])
def updateAndDelete(emp_id):
    # session.query(Customers).filter(Customers.id > 1).delete()
    # # session.rollback()
    try:
        # data = UserManagement.query.filter_by(emp_id=str(emp_id)).first()
        if request.method == "DELETE":
            db.session.query(UserManagement).filter(UserManagement.emp_id == emp_id).delete()
            # db.session.delete(data)
            db.session.commit()
            return make_response(jsonify({"msg": "UserManagement with ID successfully deleted."})), 200
        elif request.method == "PUT":
            res = request.get_json(force=True)
            print(res)
            updateData = {}
            keys = res.keys()
            if "emp_id" in keys:
                updateData[UserManagement.emp_id] = res["emp_id"]
            if "name" in keys:
                updateData[UserManagement.name] = res["name"]
            if "roll" in keys:
                updateData[UserManagement.roll] = res["roll"]
            if "email" in keys:
                updateData[UserManagement.email] = res["email"]

            is_updated = db.session.query(UserManagement).filter(UserManagement.emp_id == emp_id).update(updateData)
            db.session.commit()
            if is_updated:
                return make_response({"msg":"emp_id: " + emp_id + " successfully updated"}), 200
            else:
                return make_response({"msg":"emp_id: " + emp_id + " unable to update"}), 401

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401
