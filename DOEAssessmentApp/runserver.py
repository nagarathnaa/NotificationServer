"""
This script runs calls the create app method having endpoint blueprints as args
"""

import DOEAssessmentApp
from DOEAssessmentApp.DOE_views.email_configuration_view import emailconfig
from DOEAssessmentApp.DOE_views.rbac_view import rbac
from DOEAssessmentApp.DOE_views.company_details_view import companydetails
from DOEAssessmentApp.DOE_views.company_user_details_view import companyuserdetails
from DOEAssessmentApp.DOE_views.project_view import project
from DOEAssessmentApp.DOE_views.area_view import area
from DOEAssessmentApp.DOE_views.functionality_view import functionality_view
from DOEAssessmentApp.DOE_views.sub_functionality_view import sub_functionality_view
from DOEAssessmentApp.DOE_views.user_management_view import user_management_view
from DOEAssessmentApp.DOE_views.assessment_view import assigningteammember
from DOEAssessmentApp.DOE_views.project_assignment_to_manager_view import assigningprojectmanager
from DOEAssessmentApp.DOE_views.question_view import question
from DOEAssessmentApp.DOE_views.trn_team_member_assessment_view import assessment
from DOEAssessmentApp.DOE_views.reports_view import reports
from DOEAssessmentApp.DOE_views.tools_login_views import loginconfig
from DOEAssessmentApp.DOE_views.tools_jenkins_view import tools
from DOEAssessmentApp.DOE_views.tools_github_view import gits

bp_list = [emailconfig, rbac, companydetails, companyuserdetails, project, area, functionality_view,
           sub_functionality_view, user_management_view, assigningteammember, assigningprojectmanager,
           question, assessment, reports, loginconfig, tools, gits]

app = DOEAssessmentApp.create_app(blue_print_list=bp_list)
