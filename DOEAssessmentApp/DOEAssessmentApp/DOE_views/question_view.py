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
                        return make_response(jsonify({"msg": f"Question {quesname} successfully inserted."})), 201
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
        return make_response(jsonify({"msg": str(e)})), 400


@question.route('/api/updelquestion', methods=['PUT', 'DELETE'])
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
                questionid = res['questionid']
                data = Question.query.filter_by(id=questionid).first()
                if data is None:
                    return make_response(jsonify({"msg": "Incorrect ID"})), 404
                else:
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
                        if existing_question is None:
                            data.name = quesname
                            data.answer_type = answertype
                            data.answers = answers
                            data.maxscore = maxscore
                            data.combination = combination
                            db.session.add(data)
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
                    elif request.method == 'DELETE':
                        db.session.delete(data)
                        db.session.commit()
                        return make_response(
                            jsonify({"msg": f"Question with ID {questionid} successfully deleted."})), 204
            else:
                return make_response(jsonify({"msg": resp})), 401
        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401

    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400


@question.route('/api/viewquestion', methods=['POST'])
def getviewquestion():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Companyuserdetails.decode_auth_token(auth_token)
            if isinstance(resp, str):
                if request.method == "POST":
                    res = request.get_json(force=True)
                    proj_id = res['proj_id']
                    area_id = res['area_id']
                    func_id = res['func_id']
                    subfunc_id = res['subfunc_id']

                    data = Question.query.filter(Question.proj_id == proj_id, Question.area_id == area_id,
                                                 Question.func_id == func_id, Question.subfunc_id == subfunc_id)
                    lists = []
                    for user in data:
                        json_data = {'name': user.name, 'answer_type': user.answer_type, 'maxscore': user.maxscore,
                                     'updationdatetime': user.updationdatetime}
                        lists.append(json_data)
                    return make_response(jsonify(lists)), 200
            else:
                return make_response(jsonify({"msg": resp})), 401

        else:
            return make_response(jsonify({"msg": "Provide a valid auth token."})), 401
    except Exception as e:
        return make_response(jsonify({"msg": str(e)})), 400
