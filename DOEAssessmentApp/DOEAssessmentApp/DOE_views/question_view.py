from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.question_model import Question
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

question = Blueprint('question', __name__)

colsquestion = ['id', 'name', 'answer_type', 'answers', 'subfunc_id', 'func_id', 'area_id', 'proj_id',
                'creationdatetime', 'updationdatetime']


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
                    return jsonify({"data": result})
                elif request.method == "POST":
                    res = request.get_json(force=True)
                    quesname = res['QuestionName']
                    answertype = res['AnswerType']
                    answers = res['Answers']
                    subfuncid = res['subfunc_id']
                    funcid = res['func_id']
                    areaid = res['area_id']
                    projid = res['proj_id']
                    existing_project = Question.query.filter(Question.name == quesname, Question.subfunc_id == subfuncid
                                                             | Question.func_id == funcid).one_or_none()
                    if existing_project is None:
                        quesins = Question(quesname, answertype, answers, subfuncid, funcid, areaid, projid)
                        db.session.add(quesins)
                        db.session.commit()
                        return jsonify({"message": f"Question {quesname} successfully inserted."})
                    else:
                        if subfuncid:
                            data_sub = Subfunctionality.query.filter_by(id=subfuncid).first()
                            return jsonify({"message": f"Question {quesname} already exists for subfunctionality "
                                                       f"{data_sub.name}."})
                        elif funcid:
                            data_func = Functionality.query.filter_by(id=funcid).first()
                            return jsonify({"message": f"Question {quesname} already exists for functionality "
                                                       f"{data_func.name}."})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e
