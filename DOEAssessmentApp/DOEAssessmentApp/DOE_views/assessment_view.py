from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

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
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
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
            else:
                return jsonify({"msg": resp})
        else:
            return jsonify({"msg": "Provide a valid auth token."})
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@assigningteammember.route('/api/associateteammember/', methods=['PUT'])
def updateAndDelete():
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
            else:
                return jsonify({"msg": resp})
        else:
            return jsonify({"msg": "Provide a valid auth token."})
    except Exception as e:
        return e
