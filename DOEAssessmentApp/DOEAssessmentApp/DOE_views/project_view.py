from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_model import Project, Level
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.company_details_model import Companydetails

project = Blueprint('project', __name__)

colsproject = ['id', 'name', 'description', 'companyid', 'assessmentcompletion', 'achievedpercentage',
               'creationdatetime', 'updationdatetime']


@project.route('/api/project', methods=['GET', 'POST'])
def getaddproject():
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
                    data = Project.query.all()
                    result = [{col: getattr(d, col) for col in colsproject} for d in data]
                    return jsonify({"data": result})
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    projname = res['ProjectName']
                    projdesc = res['ProjectDescription']
                    comp_id = res['CompanyID']
                    levels = res['Levels']
                    existing_project = Project.query.filter(Project.name == projname,
                                                            Project.companyid == comp_id).one_or_none()
                    if existing_project is None:
                        projins = Project(projname, projdesc, comp_id)
                        db.session.add(projins)
                        db.session.commit()
                        for l in levels:
                            levelname = l['Name']
                            range_f = l['RangeFrom']
                            range_t = l['RangeTo']
                            combination = projins.id + levelname + range_f + "-" + range_t
                            existing_level = Level.query.filter(Level.combination == combination,
                                                                Level.project_id == projins.id).one_or_none()
                            if existing_level is None:
                                levelins = Level(levelname, range_f, range_t, combination, projins.id)
                                db.session.add(levelins)
                                db.session.commit()
                            else:
                                return jsonify({"message": f"Level {levelname} already present for {projname}."})
                        return jsonify({"message": f"Project {projname} successfully inserted."})
                    else:
                        data_comp = Companydetails.query.filter_by(id=comp_id).first()
                        return jsonify({"message": f"Project {projname} already exists for company "
                                                   f"{data_comp.companyname}."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e


@project.route('/api/updelproject/', methods=['GET', 'PUT', 'DELETE'])
def updelproject():
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
                projid = res['projectid']
                data = Project.query.filter_by(id=projid).first()
                if data is None:
                    return jsonify({"message": "Incorrect ID"})
                else:
                    if request.method == 'GET':
                        result = [{col: getattr(d, col) for col in colsproject} for d in data]
                        return jsonify({"data": result[0]})
                    elif request.method == 'PUT':
                        projectname = res['ProjectName']
                        compid = res['CompanyID']
                        levels = res['Levels']
                        existing_project = Project.query.filter(Project.name == projectname,
                                                                Project.companyid == compid).one_or_none()
                        if existing_project is None:
                            data.name = projectname
                            db.session.add(data)
                            db.session.commit()
                            for l in levels:
                                levelname = l['Name']
                                range_f = l['RangeFrom']
                                range_t = l['RangeTo']
                                combination = projid + levelname + range_f + "-" + range_t
                                existing_level = Level.query.filter(Level.combination == combination,
                                                                    Level.project_id == projid).one_or_none()
                                if existing_level is None:
                                    levelins = Level(levelname, range_f, range_t, combination, projid)
                                    db.session.add(levelins)
                                    db.session.commit()
                                else:
                                    return jsonify({"message": f"Level {levelname} already present for {projectname}."})
                            return jsonify({"message": f"Project {projectname} successfully updated."})
                        else:
                            data_comp = Companydetails.query.filter_by(id=compid).first()
                            return jsonify({"message": f"Project {projectname} already exists for company "
                                                       f"{data_comp.companyname}."})
                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        data_level = Level.query.filter_by(project_id=projid)
                        if data_level is not None:
                            for dl in data_level:
                                db.session.delete(dl)
                                db.session.commit()
                        data_area = Area.query.filter_by(projectid=projid)
                        if data_area is not None:
                            for a in data_area:
                                db.session.delete(a)
                                db.session.commit()
                        data_func = Functionality.query.filter_by(proj_id=projid)
                        if data_func is not None:
                            for f in data_func:
                                db.session.delete(f)
                                db.session.commit()
                        data_subfunc = Subfunctionality.query.filter_by(proj_id=projid)
                        if data_subfunc is not None:
                            for s in data_subfunc:
                                db.session.delete(s)
                                db.session.commit()
                        return jsonify({"message": f"Project with ID {projid} successfully deleted."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e


@project.route('/api/deletelevelforproject/', methods=['DELETE'])
def deletelevelforproject():
    try:
        if request.method == 'DELETE':
            res = request.get_json(force=True)
            levelid = res['levelid']
            data = Level.query.filter_by(id=levelid).first()
            if data is None:
                return jsonify({"message": "Incorrect ID"})
            else:
                db.session.delete(data)
                db.session.commit()
                return jsonify({"message": f"Level with ID {levelid} successfully deleted."})
    except Exception as e:
        return e

