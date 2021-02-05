FROM ubuntu:18.04
MAINTAINER mohan@devopsenabler.com
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-psycopg2 gunicorn3
WORKDIR /opt/docker/doeassessmemtapp/
COPY . .
RUN pip3 install -r requirements.txt
CMD ["gunicorn3", "-b","--timeout 150","--keep-alive 300" "0.0.0.0:5000", "wsgi:app", "--workers=3" ]