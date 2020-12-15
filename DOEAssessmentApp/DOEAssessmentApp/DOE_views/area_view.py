from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

area = Blueprint('area', __name__)

colsarea = ['id', 'name', 'description', 'projectid', 'creationdatetime', 'updationdatetime']


@area.route('/api/area', methods=['GET', 'POST'])
def getaddarea():
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
                    data = Area.query.all()
                    result = [{col: getattr(d, col) for col in colsarea} for d in data]
                    return jsonify({"data": result})
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    areaname = res['AreaName']
                    areadesc = res['AreaDescription']
                    proj_id = res['ProjectID']
                    existing_area = Area.query.filter(Area.name == areaname, Area.projectid == proj_id).one_or_none()
                    if existing_area is None:
                        areains = Area(areaname, areadesc, proj_id)
                        db.session.add(areains)
                        db.session.commit()
                        return jsonify({"message": f"Area {areaname} successfully inserted."})
                    else:
                        data_proj = Project.query.filter_by(id=proj_id).first()
                        return jsonify({"message": f"Area {areaname} already exists for project {data_proj.name}."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e


@area.route('/api/updelarea/', methods=['GET', 'PUT', 'DELETE'])
def updelarea():
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
                areaid = res['areaid']
                data = Area.query.filter_by(id=areaid).first()
                if data is None:
                    return jsonify({"message": "Incorrect ID"})
                else:
                    # if request.method == 'GET':
                    #     result = [{col: getattr(d, col) for col in colsarea} for d in data]
                    #     return jsonify({"data": result[0]})
                    if request.method == 'PUT':
                        areaname = res['AreaName']
                        proj_id = res['ProjectID']
                        existing_area = Area.query.filter(Area.name == areaname,
                                                          Area.projectid == proj_id).one_or_none()
                        if existing_area is None:
                            data.name = areaname
                            db.session.add(data)
                            db.session.commit()
                            return jsonify({"message": f"Area {areaname} successfully updated."})
                        else:
                            data_proj = Project.query.filter_by(id=proj_id).first()
                            return jsonify({"message": f"Area {areaname} already exists for project {data_proj.name}."})
                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        data_func = Functionality.query.filter_by(area_id=areaid)
                        if data_func is not None:
                            for f in data_func:
                                db.session.delete(f)
                                db.session.commit()
                        data_subfunc = Subfunctionality.query.filter_by(area_id=areaid)
                        if data_subfunc is not None:
                            for s in data_subfunc:
                                db.session.delete(s)
                                db.session.commit()
                        return jsonify({"message": f"Area with ID {areaid} successfully deleted."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e
