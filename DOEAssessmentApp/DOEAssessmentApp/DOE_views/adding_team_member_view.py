from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.adding_team_member_model import AddingTeamMember

adding_team_member_view = Blueprint('adding_team_member_view', __name__)

colsaddteam = ['id', 'emp_id', 'projectid', 'area_id',
               'functionality_id', 'subfunctionality_id',  'combination', 'creationdatetime', 'updationdatetime']


@adding_team_member_view.route('/api/addingteammember', methods=['GET', 'POST'])
def getAndPost():
    try:
        if request.method == "GET":
            data = AddingTeamMember.query.all()
            result = [{col: getattr(d, col) for col in colsaddteam} for d in data]
            return make_response(jsonify(result)), 200
        elif request.method == "POST":
            res = request.get_json(force=True)
            team_empid = res['emp_id']
            projid = res['projectid']
            areaid = res['area_id']
            funcid = res['functionality_id']
            if "subfunc_id" in res:
                subfuncid = res['subfunc_id']
                combination = str(team_empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
            else:
                subfuncid = None
                combination = str(team_empid) + str(projid) + str(areaid) + str(funcid)

            existing_team_member = AddingTeamMember.query.filter(
                AddingTeamMember.combination == combination).one_or_none()

            if existing_team_member is None:
                addingteammember = AddingTeamMember(team_empid, projid, areaid, funcid,subfuncid, combination)
                db.session.add(addingteammember)
                db.session.commit()
                return make_response(jsonify({"msg": "Team Member successfully assigned."})), 201
            else:
                return make_response(jsonify({"msg": "Team Member was already assigned before."})), 200

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@adding_team_member_view.route('/api/updateaddingteammember/', methods=['PUT'])
def updateAndDelete():
    try:
        res = request.get_json(force=True)
        row_id = res['row_id']
        data = AddingTeamMember.query.filter_by(id=row_id).first()
        if data is None:
            return jsonify({"msg": "Incorrect ID"})
        else:
            if request.method == 'PUT':
                associate_status = res['associate_status']
                if associate_status == 1:
                    data.status = 1
                    db.session.add(data)
                    db.session.commit()
                    return jsonify({"msg": "Team Member associated successfully "})
                else:
                    data.status = 0
                    db.session.add(data)
                    db.session.commit()
                    return jsonify({"msg": "Team Member disassociated successfully"})



    except Exception as e:
        return e
