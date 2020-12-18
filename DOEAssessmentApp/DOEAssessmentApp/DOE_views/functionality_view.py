from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality

functionality_view = Blueprint('functionality_view', __name__)


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@functionality_view.route('/api/functionality', methods=['GET', 'POST'])
def getAndPost():
    try:
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
                                      {'assessmentcompletion': user.assessment_completion},
                                      {'achievedpercentage': user.achieved_percentage},
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
                return make_response(
                    jsonify({"msg": "Functionality successfully inserted."})), 201
            else:
                data_area = Area.query.filter_by(id=func_area_id).first()
                return jsonify({
                    "msg": f"functionality {func_name} already exists for area {data_area.name}."})
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@functionality_view.route('/api/updelfunctionality/', methods=['PUT', 'DELETE'])
def updateAndDelete():
    try:
        res = request.get_json(force=True)
        functionalityid = res['functionalityid']
        data = Functionality.query.filter_by(id=functionalityid).first()
        if data is None:
            return jsonify({"msg": "Incorrect ID"})
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
                    return jsonify({"msg": f"functionality {func_name} successfully updated."})
                else:
                    data_area = Area.query.filter_by(id=func_area_id).first()
                    return jsonify({"msg": f"functionality {func_name} already exists for area {data_area.name}."})

            elif request.method == 'DELETE':
                db.session.delete(data)
                db.session.commit()
                data_subfunc = Subfunctionality.query.filter_by(func_id=functionalityid)
                if data_subfunc is not None:
                    for s in data_subfunc:
                        db.session.delete(s)
                        db.session.commit()
                return jsonify({"msg": f"Functionality with ID {functionalityid} successfully deleted."})



    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 401


@functionality_view.route('/api/getfunctionalitybyareaid/', methods=['GET'])
def getfunctionalitybyareaid():
    try:
        if request.method == "GET":
            res = request.get_json(force=True)
            areaid = res['AreaID']
            results = []
            data = Functionality.query.filter_by(area_id=areaid).all()
            if data is None:
                return jsonify({"msg": "No Functionalities present in the selected Area!!"})
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
    except Exception as e:
        return e

