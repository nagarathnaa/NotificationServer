from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.question_model import Question

sub_functionality_view = Blueprint('sub_functionality_view', __name__)

cols_subfunc = ['id', 'name', 'description', 'retake_assessment_days', 'func_id', 'area_id', 'proj_id',
                'assessmentcompletion', 'achievedpercentage', 'creationdatetime', 'updationdatetime']


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
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    data = Subfunctionality.query.all()
                    result = [{col: getattr(d, col) for col in cols_subfunc} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    subfunc_name = res['name']
                    subfunc_desc = res['description']
                    subfunc_retake_assess = res['retake_assessment_days']
                    subfunc_func_id = res['func_id']
                    subfunc_area_id = res['area_id']
                    subfunc_pro_id = res['proj_id']
                    existing_subfunctionality = Subfunctionality.query.filter(Subfunctionality.name ==
                                                                              subfunc_name,
                                                                              Subfunctionality.func_id ==
                                                                              subfunc_func_id).one_or_none()
                    if existing_subfunctionality is None:
                        subfuncins = Subfunctionality(subfunc_name, subfunc_desc, subfunc_retake_assess,
                                                      subfunc_func_id, subfunc_area_id, subfunc_pro_id)
                        db.session.add(subfuncins)
                        db.session.commit()
                        data = Subfunctionality.query.filter_by(id=subfuncins.id)
                        result = [{col: getattr(d, col) for col in cols_subfunc} for d in data]
                        return make_response(jsonify({"msg": f"Functionality {subfunc_name}  successfully inserted.",
                                                      "data": result[0]})), 201
                    else:

                        data_func = Functionality.query.filter_by(id=subfunc_func_id).first()
                        return make_response(jsonify({"msg": f"subfunctionality {subfunc_name} already exists "
                                                             f"for functionality {data_func.name}."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@sub_functionality_view.route('/api/updelsubfunctionality/', methods=['POST', 'PUT', 'DELETE'])
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
                data = Subfunctionality.query.filter_by(id=row_id)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'POST':
                        result = [{col: getattr(d, col) for col in cols_subfunc} for d in data]
                        return make_response(jsonify({"data": result[0]})), 200
                    elif request.method == 'PUT':
                        subfunc_name = res['name']
                        subfunc_func_id = res['func_id']
                        existing_subfunctionality = Subfunctionality.query.filter(Subfunctionality.name ==
                                                                                  subfunc_name,
                                                                                  Subfunctionality.func_id ==
                                                                                  subfunc_func_id).one_or_none()
                        if existing_subfunctionality is None:
                            data.first().name = subfunc_name
                            db.session.add(data.first())
                            db.session.commit()
                            return make_response(jsonify({"msg": f"subfunctionality {subfunc_name} successfully "
                                                                 f"updated."})), 200
                        else:
                            data_func = Functionality.query.filter_by(id=subfunc_func_id).first()
                            return make_response(jsonify({"msg": f"subfunctionality {subfunc_name} already exists "
                                                                 f"for area {data_func.name}."})), 400
                    elif request.method == 'DELETE':
                        db.session.delete(data.first())
                        db.session.commit()
                        data_question = Question.query.filter_by(subfunc_id=row_id)
                        if data_question is not None:
                            for question in data_question:
                                db.session.delete(question)
                                db.session.commit()
                        return make_response(jsonify({"msg": f"Subfunctionality with ID {row_id} "
                                                             f"successfully deleted."})), 204
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@sub_functionality_view.route('/api/getsubfunctionalitybyfunctionalityid/', methods=['POST'])
def getsubfunctionalitybyfunctionalityid():
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
                    funcid = res['FunctionalityID']
                    results = []
                    data = Subfunctionality.query.filter_by(func_id=funcid).all()
                    if data is None:
                        return make_response(jsonify({"msg": "No Sub-functionalities present in the "
                                                             "selected Functionality!!"})), 404
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
                        return make_response(jsonify({"data": results})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
