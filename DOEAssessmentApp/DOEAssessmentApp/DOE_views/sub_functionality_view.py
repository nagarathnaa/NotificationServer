from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.question_model import Question

sub_functionality_view = Blueprint('sub_functionality_view', __name__)


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@sub_functionality_view.route('/api/subfunctionality', methods=['GET', 'POST'])
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
                    data = Subfunctionality.query.all()
                    for user in data:
                        json_data = mergedict({'id': user.id},
                                              {'name': user.name},
                                              {'description': user.description},
                                              {'retake_assessment_days': user.retake_assessment_days},
                                              {'func_id': user.func_id},
                                              {'area_id': user.area_id},
                                              {'proj_id': user.proj_id},
                                              {'assessmentcompletion': user.assessment_completion},
                                              {'achievedpercentage': user.achieved_percentage},
                                              {'creationdatetime':user.creationdatetime},
                                              {'updationdatetime':user.updationdatetime})
                        results.append(json_data)
                    return make_response(jsonify(results)), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    subfunc_name = res['name']
                    subfunc_desc = res['description']
                    subfunc_retake_assess = res['retake_assessment_days']
                    subfunc_func_id = res['func_id']
                    subfunc_area_id = res['area_id']
                    subfunc_pro_id = res['proj_id']
                    existing_subfunctionality = Subfunctionality.query.filter(Subfunctionality.name == subfunc_name,
                                                                              Subfunctionality.func_id == subfunc_func_id ).one_or_none()
                    if existing_subfunctionality is None:
                        subfuncins = Subfunctionality(subfunc_name, subfunc_desc, subfunc_retake_assess,subfunc_func_id, subfunc_area_id, subfunc_pro_id)
                        db.session.add(subfuncins)
                        db.session.commit()
                        return make_response(
                            jsonify({"msg": f"SubFunctionality {subfunc_name} successfully inserted."})), 201
                    else:

                        data_func = Functionality.query.filter_by(id=subfunc_func_id).first()
                        return jsonify({
                            "msg": f"subfunctionality {subfunc_name} already exists for functionality {data_func.name}."})
            else:
                return jsonify({"msg": resp})
        else:
            return jsonify({"msg": "Provide a valid auth token."})
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@sub_functionality_view.route('/api/updelsubfunctionality/', methods=['PUT', 'DELETE'])
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
                sub_functionalityid = res['sub_functionalityid']
                data = Subfunctionality.query.filter_by(id=sub_functionalityid).first()
                if data is None:
                    return jsonify({"msg": "Incorrect ID"})
                else:
                    if request.method == 'PUT':
                        subfunc_name = res['name']
                        subfunc_func_id = res['func_id']
                        existing_subfunctionality = Subfunctionality.query.filter(Subfunctionality.name == subfunc_name,
                                                                                  Subfunctionality.func_id == subfunc_func_id).one_or_none()
                        if existing_subfunctionality is None:
                            data.name = subfunc_name
                            db.session.add(data)
                            db.session.commit()
                            return jsonify({"msg": f"subfunctionality {subfunc_name} successfully updated."})
                        else:
                            data_func = Functionality.query.filter_by(id=subfunc_func_id).first()
                            return jsonify({"msg": f"subfunctionality {subfunc_name} already exists for area {data_func.name}."})

                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        data_question = Question.query.filter_by(subfunc_id=sub_functionalityid)
                        if data_question is not None:
                            for q in data_question:
                                db.session.delete(q)
                                db.session.commit()
                        return jsonify({"msg": f"Subfunctionality with ID {sub_functionalityid} successfully deleted."})
            else:
                return jsonify({"msg": resp})
        else:
            return jsonify({"msg": "Provide a valid auth token."})


    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@sub_functionality_view.route('/api/getsubfunctionalitybyfunctionalityid/', methods=['GET'])
def getsubfunctionalitybyfunctionalityid():
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
                    funcid = res['FunctionalityID']
                    results = []
                    data = Subfunctionality.query.filter_by(func_id=funcid).all()
                    if data is None:
                        return jsonify({"msg": "No Sub-functionalities present in the selected Functionality!!"})
                    else:
                        for d in data:
                            json_data = mergedict({'id': d.id},
                                                  {'name': d.name},
                                                  {'description': d.description},
                                                  {'retake_assessment_days': d.retake_assessment_days},
                                                  {'func_id': d.func_id},
                                                  {'area_id': d.area_id},
                                                  {'proj_id': d.proj_id},
                                                  {'assessmentcompletion': d.assessment_completion},
                                                  {'achievedpercentage': d.achieved_percentage},
                                                  {'creationdatetime': d.creationdatetime},
                                                  {'updationdatetime': d.updationdatetime})
                            results.append(json_data)
                        return make_response(jsonify(results)), 200
            else:
                return jsonify({"msg": resp})
        else:
            return jsonify({"msg": "Provide a valid auth token."})
    except Exception as e:
        return e
