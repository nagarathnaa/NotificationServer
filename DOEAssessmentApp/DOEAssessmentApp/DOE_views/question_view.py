from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

question = Blueprint('question', __name__)

colsquestion = ['id', 'name', 'answer_type', 'answers', 'maxscore', 'subfunc_id', 'func_id', 'area_id', 'proj_id',
                'combination', 'creationdatetime', 'updationdatetime']


@question.route('/api/question', methods=['GET', 'POST'])
def getaddquestion():
    """
        ---
        get:
          description: Fetch question(s).
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
              - getcreatequestion
        post:
          description: Create a question.
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
              - getcreatequestion
    """
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
                    data = Question.query.all()
                    result = [{col: getattr(d, col) for col in colsquestion} for d in data]
                    return make_response(jsonify({"data": result})), 200
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    quesname = res['QuestionName']
                    answertype = res['AnswerType']
                    answers = res['Answers']
                    maxscore = res["MaxScore"]
                    funcid = res['func_id']
                    areaid = res['area_id']
                    projid = res['proj_id']
                    if "subfunc_id" in res:
                        subfuncid = res['subfunc_id']
                        combination = str(projid) + str(areaid) + str(funcid) + str(subfuncid) + str(quesname)
                    else:
                        subfuncid = None
                        combination = str(projid) + str(areaid) + str(funcid) + str(quesname)
                    existing_question = Question.query.filter(Question.combination == combination).one_or_none()
                    if existing_question is None:
                        quesins = Question(quesname, answertype, answers, maxscore, subfuncid, funcid, areaid, projid,
                                           combination)
                        db.session.add(quesins)
                        db.session.commit()
                        data = Question.query.filter_by(id=quesins.id)
                        result = [{col: getattr(d, col) for col in colsquestion} for d in data]
                        return make_response(jsonify({"msg": f"Question {quesname} successfully inserted.",
                                                      "data": result[0]})), 201
                    else:
                        if subfuncid:
                            data_sub = Subfunctionality.query.filter_by(id=subfuncid).first()
                            return make_response(
                                jsonify({"msg": f"Question {quesname} already exists for subfunctionality "
                                                f"{data_sub.name}."})), 400
                        elif funcid:
                            data_func = Functionality.query.filter_by(id=funcid).first()
                            return make_response(
                                jsonify({"msg": f"Question {quesname} already exists for functionality "
                                                f"{data_func.name}."})), 400
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@question.route('/api/updelquestion', methods=['POST', 'PUT', 'DELETE'])
def updateAndDelete():
    """
        ---
        post:
          description: Fetch a question.
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
              - updatedeletequestion
        put:
          description: Update a question.
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
              - updatedeletequestion
        delete:
          description: Delete a question.
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
              - updatedeletequestion
    """
    try:
        quesexists = True
        datalist = []
        data = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                res = request.get_json(force=True)
                if type(res['questionid']) is list:
                    questionid = res['questionid']
                    for q in questionid:
                        data = Question.query.filter_by(id=q)
                        if data.first() is not None:
                            datalist.append(data)
                else:
                    questionid = res['questionid']
                    data = Question.query.filter_by(id=questionid)
                    if data.first() is None:
                        quesexists = False
                if quesexists is False:
                    return make_response(jsonify({"msg": "Incorrect ID"})), 404
                else:
                    if request.method == "POST":
                        lists = []
                        if len(datalist) > 0:
                            for data in datalist:
                                for user in data:
                                    json_data = {'question_id': user.id, 'question_name': user.name,
                                                 'answer_type': user.answer_type, 'maxscore': user.maxscore,
                                                 'answers': user.answers, 'proj_id': user.proj_id,
                                                 'area_id': user.area_id,
                                                 'func_id': user.func_id, 'subfunc_id': user.subfunc_id,
                                                 'updationdatetime': user.updationdatetime}
                                    lists.append(json_data)
                        else:
                            for user in data:
                                json_data = {'question_id': user.id, 'question_name': user.name,
                                             'answer_type': user.answer_type, 'maxscore': user.maxscore,
                                             'answers': user.answers, 'proj_id': user.proj_id, 'area_id': user.area_id,
                                             'func_id': user.func_id, 'subfunc_id': user.subfunc_id,
                                             'updationdatetime': user.updationdatetime}
                                lists.append(json_data)
                        return make_response(jsonify({"data": lists})), 200
                    if request.method == 'PUT':
                        quesname = res['QuestionName']
                        answertype = res['AnswerType']
                        answers = res['Answers']
                        maxscore = res["MaxScore"]
                        funcid = res['func_id']
                        areaid = res['area_id']
                        projid = res['proj_id']
                        if "subfunc_id" in res:
                            subfuncid = res['subfunc_id']
                            combination = str(projid) + str(areaid) + str(funcid) + str(subfuncid) + str(quesname)
                        else:
                            subfuncid = None
                            combination = str(projid) + str(areaid) + str(funcid) + str(quesname)
                        existing_question = Question.query.filter(Question.combination == combination).one_or_none()
                        if quesname != data.first().name:
                            if existing_question is None:
                                data.first().name = quesname
                                data.first().answer_type = answertype
                                data.first().answers = answers
                                data.first().maxscore = maxscore
                                db.session.add(data.first())
                                db.session.commit()
                                return make_response(jsonify({"msg": f"Question {quesname} successfully updated"})), 200
                            else:
                                if subfuncid:
                                    data_sub = Subfunctionality.query.filter_by(id=subfuncid).first()
                                    return make_response(
                                        jsonify({"msg": f"Question {quesname} already exists for subfunctionality "
                                                        f"{data_sub.name}."})), 400
                                elif funcid:
                                    data_func = Functionality.query.filter_by(id=funcid).first()
                                    return make_response(
                                        jsonify({"msg": f"Question {quesname} already exists for functionality "
                                                        f"{data_func.name}."})), 400
                        else:
                            data.first().answer_type = answertype
                            data.first().answers = answers
                            data.first().maxscore = maxscore
                            db.session.add(data.first())
                            db.session.commit()
                            return make_response(jsonify({"msg": f"Question {quesname} successfully updated"})), 200
                    elif request.method == 'DELETE':
                        db.session.delete(data.first())
                        db.session.commit()
                        return make_response(
                            jsonify({"msg": f"Question with ID {questionid} successfully deleted."})), 204
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@question.route('/api/viewquestion', methods=['POST'])
def viewquestion():
    """
        ---
        post:
          description: View question(s) using required filters.
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
              - viewquestions
    """
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
                    proj_id = res['proj_id']
                    area_id = res['area_id']
                    func_id = res['func_id']
                    if 'subfunc_id' in res:
                        subfunc_id = res['subfunc_id']
                        data = Question.query.filter(Question.proj_id == proj_id, Question.area_id == area_id,
                                                     Question.func_id == func_id, Question.subfunc_id == subfunc_id,
                                                     Question.isdependentquestion == 0)
                    else:
                        data = Question.query.filter(Question.proj_id == proj_id, Question.area_id == area_id,
                                                     Question.func_id == func_id, Question.isdependentquestion == 0)
                    lists = []
                    for user in data:
                        json_data = {'question_id': user.id, 'question_name': user.name,
                                     'answer_type': user.answer_type, 'maxscore': user.maxscore,
                                     'answers': user.answers, 'proj_id': user.proj_id, 'area_id': user.area_id,
                                     'func_id': user.func_id, 'subfunc_id': user.subfunc_id,
                                     'updationdatetime': user.updationdatetime}
                        lists.append(json_data)
                    childquesidlist = []
                    for i in range(len(lists)):
                        for j in lists[i]["answers"]:
                            if j["childquestionid"] != 0:
                                if isinstance(j["childquestionid"], list):
                                    for k in j["childquestionid"]:
                                        childquesidlist.append(k)
                                else:
                                    childquesidlist.append(j["childquestionid"])
                    for c in childquesidlist:
                        for i in range(len(lists)):
                            if lists[i]["question_id"] == c:
                                lists.pop(i)
                                break
                    return make_response(jsonify({"data": lists})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500


@question.route('/api/updatequesasdependent', methods=['PUT'])
def updatequesasdependent():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if Companyuserdetails.query.filter_by(empemail=resp).first() is not None:
                if request.method == 'PUT':
                    res = request.get_json(force=True)
                    questionid = res['questionid']
                    isdependentquestion = res['isdependentquestion']
                    data = Question.query.filter_by(id=questionid)
                    data.first().isdependentquestion = isdependentquestion
                    db.session.add(data.first())
                    db.session.commit()
                    if isdependentquestion == 1:
                        return make_response(jsonify({"msg": f"Question {data.first().name} successfully updated "
                                                             f"as dependent question"})), 200
                    else:
                        return make_response(jsonify({"msg": f"Question {data.first().name} successfully updated "
                                                             f"as non-dependent question"})), 200
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 500