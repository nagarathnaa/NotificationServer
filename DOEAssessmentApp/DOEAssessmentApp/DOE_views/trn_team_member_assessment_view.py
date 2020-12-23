from flask import *
from DOEAssessmentApp import db
from DOEAssessmentApp.DOE_models.trn_team_member_assessment_model import Assessment, QuestionsAnswered

assessment = Blueprint('assessment', __name__)
