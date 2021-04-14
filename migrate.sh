#!/bin/sh
if [ -d "migrations" ]
then
  echo "true"
  python3 manage.py db migrate; python3 manage.py db upgrade
else
  echo "false"
  python3 manage.py db init; python3 manage.py db migrate; python3 manage.py db upgrade
fi