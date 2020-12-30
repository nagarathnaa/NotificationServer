from flask import *
from DOEAssessmentApp import app, db
from DOEAssessmentApp.DOE_models.assessment_model import Assessment
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

assigningteammember = Blueprint('assigningteammember', __name__)

colsaddteam = ['id', 'emp_id', 'projectid', 'area_id',
               'functionality_id', 'subfunctionality_id',
               'employeeassignedstatus', 'combination',
               'totalmaxscore', 'totalscoreachieved',
               'comment', 'assessmentstatus',
               'assessmenttakendatetime', 'assessmentrevieweddatetime',
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
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    data = Assessment.query.all()
                    result = [{col: getattr(d, col) for col in colsaddteam} for d in data]
                    return make_response(jsonify({"data": result})), 200
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
                        return make_response(jsonify({"msg": "Team Member was already assigned before."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


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
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                res = request.get_json(force=True)
                row_id = res['row_id']
                data = Assessment.query.filter_by(id=row_id).first()
                if data is None:
                    return make_response(jsonify({"msg": "Incorrect ID"})), 404
                else:
                    if request.method == 'PUT':
                        associate_status = res['associate_status']
                        if associate_status == 1:
                            data.employeeassignedstatus = 1
                            db.session.add(data)
                            db.session.commit()
                            return make_response(jsonify({"msg": "Team Member associated successfully "})), 200
                        else:
                            data.employeeassignedstatus = 0
                            db.session.add(data)
                            db.session.commit()
                            return make_response(jsonify({"msg": "Team Member disassociated successfully"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchprojectassigntoteam/', methods=['POST'])
def fetchprojectassigntoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    data = Assessment.query.distinct(Assessment.projectid).filter(Assessment.emp_id == emp_id,
                                                                                  Assessment.employeeassignedstatus
                                                                                  == 1)
                    lists = []
                    for user in data:
                        project_data = Project.query.filter(Project.id == user.projectid).first()
                        lists.append({'projectid': user.projectid, 'projectname': project_data.name})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchareanametoteam/', methods=['POST'])
def fetchareanametoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    projectid = res['projectid']
                    data = Assessment.query.distinct(Assessment.area_id).filter(Assessment.emp_id == emp_id,
                                                                                Assessment.projectid == projectid,
                                                                                Assessment.employeeassignedstatus == 1)

                    lists = []
                    for user in data:
                        area_data = Area.query.filter(Area.id == user.area_id).first()
                        lists.append({'area_id': user.area_id, 'area_name': area_data.name})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchfunctionalitynametoteam/', methods=['POST'])
def fetchfunctionalitynametoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    projectid = res['projectid']
                    area_id = res['area_id']
                    data = Assessment.query.distinct(Assessment.functionality_id).filter(Assessment.emp_id == emp_id,
                                                                                         Assessment.projectid
                                                                                         == projectid,
                                                                                         Assessment.area_id
                                                                                         == area_id,
                                                                                         Assessment.
                                                                                         employeeassignedstatus == 1)
                    lists = []
                    for user in data:
                        functionality_data = Functionality.query.filter(
                            Functionality.id == user.functionality_id).first()
                        lists.append(
                            {'functionality_id': user.functionality_id, 'functionality_name': functionality_data.name})
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@assigningteammember.route('/api/fetchSubfunctionalitynametoteam/', methods=['POST'])
def fetchSubfunctionalitynametoteam():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "POST":
                    res = request.get_json(force=True)
                    emp_id = res['emp_id']
                    projectid = res['projectid']
                    area_id = res['area_id']
                    functionality_id = res['functionality_id']
                    data = Assessment.query.distinct(Assessment.subfunctionality_id).filter(Assessment.emp_id == emp_id,
                                                                                            Assessment.projectid
                                                                                            == projectid,
                                                                                            Assessment.area_id
                                                                                            == area_id,
                                                                                            Assessment.functionality_id
                                                                                            == functionality_id,
                                                                                            Assessment.
                                                                                            employeeassignedstatus == 1)
                    lists = []
                    for user in data:
                        if user.subfunctionality_id is not None:
                            subfunc_data = Subfunctionality.query.filter(
                                Subfunctionality.id == user.subfunctionality_id).first()
                            lists.append({'sucfunc_id': user.subfunctionality_id, 'subfunc_name': subfunc_data.name})
                        else:
                            pass
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
