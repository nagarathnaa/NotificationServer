from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.project_model import Project
from DOEAssessmentApp.DOE_models.area_model import Area
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails
from DOEAssessmentApp.DOE_models.question_model import Question

area = Blueprint('area', __name__)


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


@area.route('/api/area', methods=['GET', 'POST'])
def getaddarea():
    """
        ---
        get:
          description: Fetch area(s).
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - getcreatearea
        post:
          description: Create an area.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - getcreatearea
    """
    try:
        results = []
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == "GET":
                    data = Area.query.all()
                    for d in data:
                        json_data = mergedict({'id': d.id},
                                              {'name': d.name},
                                              {'description': d.description},
                                              {'projectid': d.projectid},
                                              {'assessmentcompletion': str(d.assessmentcompletion)},
                                              {'achievedpercentage': str(d.achievedpercentage)},
                                              {'creationdatetime': d.creationdatetime},
                                              {'updationdatetime': d.updationdatetime})
                        results.append(json_data)
                    return make_response(jsonify({"data": results})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    areaname = res['name']
                    areadesc = res['description']
                    proj_id = res['projectid']
                    existing_area = Area.query.filter(Area.name == areaname, Area.projectid == proj_id).one_or_none()
                    if existing_area is None:
                        areains = Area(areaname, areadesc, proj_id)
                        db.session.add(areains)
                        db.session.commit()
                        data = Area.query.filter_by(id=areains.id)
                        for d in data:
                            json_data = mergedict({'id': d.id},
                                                  {'name': d.name},
                                                  {'description': d.description},
                                                  {'projectid': d.projectid},
                                                  {'assessmentcompletion': str(d.assessmentcompletion)},
                                                  {'achievedpercentage': str(d.achievedpercentage)},
                                                  {'creationdatetime': d.creationdatetime},
                                                  {'updationdatetime': d.updationdatetime})
                            results.append(json_data)
                        return make_response(jsonify({"message": f"Area {areaname} successfully inserted.",
                                                      "data": results[0]})), 201
                    else:
                        data_proj = Project.query.filter_by(id=proj_id).first()
                        return make_response(jsonify({"message": f"Area {areaname} already "
                                                                 f"exists for project {data_proj.name}."})), 400
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@area.route('/api/updelarea/', methods=['POST', 'PUT', 'DELETE'])
def updelarea():
    """
        ---
        post:
          description: Fetch an area.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - updatedeletearea
        put:
          description: Update an area.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - updatedeletearea
        delete:
          description: Delete an area.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - updatedeletearea
    """
    try:
        results = []
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                res = request.get_json(force=True)
                areaid = res['areaid']
                data = Area.query.filter_by(id=areaid)
                if data.first() is None:
                    return make_response(jsonify({"message": "Incorrect ID"})), 404
                else:
                    if request.method == 'POST':
                        for d in data:
                            json_data = mergedict({'id': d.id},
                                                  {'name': d.name},
                                                  {'description': d.description},
                                                  {'projectid': d.projectid},
                                                  {'assessmentcompletion': str(d.assessmentcompletion)},
                                                  {'achievedpercentage': str(d.achievedpercentage)},
                                                  {'creationdatetime': d.creationdatetime},
                                                  {'updationdatetime': d.updationdatetime})
                            results.append(json_data)
                        return jsonify({"data": results[0]})
                    if request.method == 'PUT':
                        areadesc = res['AreaDescription']
                        data.first().description = areadesc
                        db.session.add(data.first())
                        db.session.commit()
                        return make_response(jsonify({"message": f"Area {data.first().name} successfully "
                                                                 f"updated."})), 200

                    elif request.method == 'DELETE':
                        db.session.delete(data.first())
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
                        data_question = Question.query.filter_by(area_id=areaid)
                        if data_question is not None:
                            for q in data_question:
                                db.session.delete(q)
                                db.session.commit()
                        return make_response(jsonify({"message": f"Area with ID {areaid} "
                                                                 f"successfully deleted."})), 204
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@area.route('/api/getareabyprojectid/', methods=['POST'])
def getareabyprojectid():
    """
        ---
        post:
          description: Fetch areas by project id.
          parameters:
            -
              name: Authorization
              in: header
              type: string
              required: true
          requestBody:
            required: true
            content:
                application/json:
                    schema: InputSchema
          responses:
            '200':
              description: call successful
              content:
                application/json:
                  schema: OutputSchema
          tags:
              - fetchareabyprojectid
    """
    try:
        results = []
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
                    projid = res['ProjectID']
                    data = Area.query.filter_by(projectid=projid).all()
                    if data is None:
                        return make_response(jsonify({"message": "No Areas present in the selected Project!!"})), 404
                    else:
                        for d in data:
                            json_data = mergedict({'id': d.id},
                                                  {'name': d.name},
                                                  {'description': d.description},
                                                  {'projectid': d.projectid},
                                                  {'assessmentcompletion': str(d.assessmentcompletion)},
                                                  {'achievedpercentage': str(d.achievedpercentage)},
                                                  {'creationdatetime': d.creationdatetime},
                                                  {'updationdatetime': d.updationdatetime})
                            results.append(json_data)
                        return make_response(jsonify({"data": results})), 200
            else:
                return make_response(jsonify({"message": resp})), 401
        else:
            return make_response(jsonify({"message": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500
