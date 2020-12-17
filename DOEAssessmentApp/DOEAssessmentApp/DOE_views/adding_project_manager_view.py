from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.adding_project_manager_model import AddingProjectManager

adding_project_manager_view = Blueprint('adding_project_manager_view', __name__)


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@adding_project_manager_view.route('/api/addingprojectmanager', methods=['GET', 'POST'])
def getAndPost():
    try:
        if request.method == "GET":
            results = []
            data = AddingProjectManager.query.all()
            for user in data:
                json_data = mergedict({'id': user.id}, {'emp_id': user.emp_id}, {'project_id': user.project_id},
                                      {'status': user.status}, {'creationdatetime': user.creationdatetime},
                                      {'updationdatetime': user.updationdatetime})
                results.append(json_data)

            return make_response(jsonify(results)), 200
        elif request.method == "POST":
            res = request.get_json(force=True)
            pm_id = res['emp_id']
            pm_project_id = res['project_id']
            existing_projectmanager = AddingProjectManager.query.filter(AddingProjectManager.emp_id == pm_id,
                                                                        AddingProjectManager.project_id == pm_project_id).one_or_none()

            if existing_projectmanager is None:
                project_managers_in = AddingProjectManager(pm_id, pm_project_id)
                db.session.add(project_managers_in)
                db.session.commit()
                return make_response(jsonify({"msg": "project manager successfully assigned."})), 201
            else:

                return jsonify(
                    {"message": f"project manager was already assigned before."})

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@adding_project_manager_view.route('/api/editaddingprojectmanager/', methods=['PUT'])
def updateAndDelete():
    try:
        res = request.get_json(force=True)
        row_id = res['row_id']
        data = AddingProjectManager.query.filter_by(id=row_id).first()
        if data is None:
            return jsonify({"msg": "Incorrect ID"})
        else:
            if request.method == 'PUT':
                associate_status = res['associate_status']
                if associate_status == 1:
                    data.status = 1
                    db.session.add(data)
                    db.session.commit()
                    return jsonify({"msg": "project manager associated successfully "})
                else:
                    data.status = 0
                    db.session.add(data)
                    db.session.commit()
                    return jsonify({"msg": "project manager disassociated successfully"})


    except Exception as e:
        return e
