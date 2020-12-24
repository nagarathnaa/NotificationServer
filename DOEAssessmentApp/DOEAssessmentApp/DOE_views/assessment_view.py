from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment

assigningteammember = Blueprint('assigningteammember', __name__)

colsaddteam = ['id', 'emp_id', 'projectid', 'area_id',
               'functionality_id', 'subfunctionality_id',
               'employeeassignedstatus', 'combination',
               'totalscoreacheived', 'comment',
               'assessmentstatus', 'assessmenttakendatetime', 'assessmentrevieweddatetime',
               'creationdatetime', 'updationdatetime']


@assigningteammember.route('/api/assigningteammember', methods=['GET', 'POST'])
def getAndPost():
    try:
        if request.method == "GET":
            data = Assessment.query.all()
            result = [{col: getattr(d, col) for col in colsaddteam} for d in data]
            return make_response(jsonify(result)), 200
        elif request.method == "POST":
            res = request.get_json(force=True)
            team_empid = res['emp_id']
            projid = res['projectid']
            areaid = res['area_id']
            funcid = res['functionality_id']
            assessmentstatus = 'NEW'
            if "subfunc_id" in res:
                subfuncid = res['subfunc_id']
                combination = str(team_empid) + str(projid) + str(areaid) + str(funcid) + str(subfuncid)
            else:
                subfuncid = None
                combination = str(team_empid) + str(projid) + str(areaid) + str(funcid)

            existing_assessment = Assessment.query.filter(Assessment.combination == combination).one_or_none()

            if existing_assessment is None:
                assessmentins = Assessment(team_empid, projid, areaid, funcid, subfuncid, combination,
                                           assessmentstatus)
                db.session.add(assessmentins)
                db.session.commit()
                return make_response(jsonify({"msg": "Team Member successfully assigned."})), 201
            else:
                return make_response(jsonify({"msg": "Team Member was already assigned before."})), 200
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@assigningteammember.route('/api/associateteammember/', methods=['PUT'])
def updateAndDelete():
    try:
        res = request.get_json(force=True)
        row_id = res['row_id']
        data = Assessment.query.filter_by(id=row_id).first()
        if data is None:
            return jsonify({"msg": "Incorrect ID"})
        else:
            if request.method == 'PUT':
                associate_status = res['associate_status']
                if associate_status == 1:
                    data.employeeassignedstatus = 1
                    db.session.add(data)
                    db.session.commit()
                    return jsonify({"msg": "Team Member associated successfully "})
                else:
                    data.employeeassignedstatus = 0
                    db.session.add(data)
                    db.session.commit()
                    return jsonify({"msg": "Team Member disassociated successfully"})
    except Exception as e:
        return e
