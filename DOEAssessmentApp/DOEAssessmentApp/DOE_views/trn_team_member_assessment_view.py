from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.trn_team_member_assessment_model import Assessment, QuestionsAnswered
from DOEAssessmentApp.DOE_models.functionality_model import Functionality
from DOEAssessmentApp.DOE_models.sub_functionality_model import Subfunctionality
from DOEAssessmentApp.DOE_models.company_user_details_model import Companyuserdetails

assessment = Blueprint('assessment', __name__)


@assessment.route('/api/submitassessment', methods=['POST'])
def submitassessment():
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
                    empid = res['EmployeeID']
                    projid = res['proj_id']
                    areaid = res['area_id']
                    funcid = res['func_id']
                    status = "SUBMITTED"
                    questions = res['Questions']
                    if 'subfunc_id' in res:
                        subfuncid = res['subfunc_id']
                        existing_assessment = Assessment.query.filter(Assessment.projectid == projid,
                                                                      Assessment.area_id == areaid,
                                                                      Assessment.functionality_id ==
                                                                      funcid,
                                                                      Assessment.subfunctionality_id ==
                                                                      subfuncid,
                                                                      Assessment.emp_id == empid).one_or_none()
                    else:
                        subfuncid = None
                        existing_assessment = Assessment.query.filter(Assessment.projectid == projid,
                                                                      Assessment.area_id == areaid,
                                                                      Assessment.functionality_id ==
                                                                      funcid,
                                                                      Assessment.emp_id == empid).one_or_none()
                    if existing_assessment is None:
                        assesssub = Assessment(empid, projid, areaid, funcid, subfuncid, status)
                        db.session.add(assesssub)
                        db.session.commit()
                        for q in questions:
                            qid = q['QID']
                            selectedoptions = q['selectedoptions']
                            scoreacheived = q['scoreacheived']
                            quesanssubmit = QuestionsAnswered(qid, selectedoptions, scoreacheived, assesssub.id)
                            db.session.add(quesanssubmit)
                            db.session.commit()
                        return jsonify({"message": f"Assessment submitted successfully!!"})
                    else:
                        if subfuncid:
                            data_sub = Subfunctionality.query.filter_by(id=subfuncid).first()
                            return jsonify({"message": f"Assessment was already submitted for subfunctionality "
                                                       f"{data_sub.name}!!"})
                        else:
                            data_func = Functionality.query.filter_by(id=funcid).first()
                            return jsonify({"message": f"Assessment was already submitted for functionality "
                                                       f"{data_func.name}!!"})
            else:
                return jsonify({"message": resp})
        else:
            return jsonify({"message": "Provide a valid auth token."})
    except Exception as e:
        return e
