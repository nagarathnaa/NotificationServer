#!/bin/sh
if [ -d "migrations" ]
then
  echo "true"
  python3 DOEAssessmentApp/manage.py db migrate; python3 DOEAssessmentApp/manage.py db upgrade
else
  echo "false"
  python3 DOEAssessmentApp/manage.py db init; python3 DOEAssessmentApp/manage.py db migrate; python3 DOEAssessmentApp/manage.py db upgrade
fi