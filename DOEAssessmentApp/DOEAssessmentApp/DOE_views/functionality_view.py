from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.question_model import Question

functionality_view = Blueprint('functionality_view', __name__)


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@functionality_view.route('/api/functionality', methods=['GET', 'POST'])
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
                    results = []
                    data = Functionality.query.all()
                    for user in data:
                        json_data = mergedict({'id': user.id},
                                              {'name': user.name},
                                              {'description': user.description},
                                              {'retake_assessment_days': user.retake_assessment_days},
                                              {'area_id': user.area_id},
                                              {'proj_id': user.proj_id},
                                              {'assessmentcompletion': user.assessmentcompletion},
                                              {'achievedpercentage': user.achievedpercentage},
                                              {'creationdatetime': user.creationdatetime},
                                              {'updationdatetime': user.updationdatetime})
                        results.append(json_data)
                    return make_response(jsonify(results)), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    func_name = res['name']
                    func_desc = res['description']
                    func_retake_assess = res['retake_assessment_days']
                    func_area_id = res['area_id']
                    func_pro_id = res['proj_id']
                    existing_functionality = Functionality.query.filter(Functionality.name == func_name,
                                                                        Functionality.area_id == func_area_id).one_or_none()
                    if existing_functionality is None:
                        funcins = Functionality(func_name, func_desc, func_retake_assess, func_area_id, func_pro_id)
                        db.session.add(funcins)
                        db.session.commit()
                        return make_response(jsonify({"msg": "Functionality successfully inserted."})), 201
                    else:
                        data_area = Area.query.filter_by(id=func_area_id).first()
                        return make_response(jsonify({"msg": f"functionality {func_name} already "
                                                             f"exists for area {data_area.name}."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@functionality_view.route('/api/updelfunctionality/', methods=['PUT', 'DELETE'])
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
                functionalityid = res['functionalityid']
                data = Functionality.query.filter_by(id=functionalityid).first()
                if data is None:
                    return make_response(jsonify({"msg": "Incorrect ID"})), 404
                else:
                    if request.method == 'PUT':
                        func_name = res['name']
                        func_area_id = res['area_id']
                        existing_functionality = Functionality.query.filter(Functionality.name == func_name,
                                                                            Functionality.area_id == func_area_id).one_or_none()
                        if existing_functionality is None:
                            data.name = func_name
                            db.session.add(data)
                            db.session.commit()
                            return make_response(jsonify({"msg": f"functionality {func_name} "
                                                                 f"successfully updated."})), 200
                        else:
                            data_area = Area.query.filter_by(id=func_area_id).first()
                            return make_response(jsonify({"msg": f"functionality {func_name} already "
                                                                 f"exists for area {data_area.name}."})), 400

                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        data_subfunc = Subfunctionality.query.filter_by(func_id=functionalityid)
                        if data_subfunc is not None:
                            for s in data_subfunc:
                                db.session.delete(s)
                                db.session.commit()
                        data_question = Question.query.filter_by(func_id=functionalityid)
                        if data_question is not None:
                            for q in data_question:
                                db.session.delete(q)
                                db.session.commit()
                        return make_response(jsonify({"msg": f"Functionality with ID {functionalityid} "
                                                             f"successfully deleted."})), 204
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@functionality_view.route('/api/getfunctionalitybyareaid/', methods=['GET'])
def getfunctionalitybyareaid():
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
                    res = request.get_json(force=True)
                    areaid = res['AreaID']
                    results = []
                    data = Functionality.query.filter_by(area_id=areaid).all()
                    if data is None:
                        return make_response(jsonify({"msg": "No Functionalities present in the "
                                                             "selected Area!!"})), 404
                    else:
                        for d in data:
                            json_data = mergedict({'id': d.id},
                                                  {'name': d.name},
                                                  {'description': d.description},
                                                  {'retake_assessment_days': d.retake_assessment_days},
                                                  {'area_id': d.area_id},
                                                  {'proj_id': d.proj_id},
                                                  {'assessmentcompletion': d.assessment_completion},
                                                  {'achievedpercentage': d.achieved_percentage},
                                                  {'creationdatetime': d.creationdatetime},
                                                  {'updationdatetime': d.updationdatetime})
                            results.append(json_data)
                        return make_response(jsonify(results)), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400
