FROM ubuntu:18.04
MAINTAINER mohan@devopsenabler.com
RUN apt-get update -y && \
    apt-get install -y python3-pip gunicorn3
WORKDIR /opt/docker/doeassessmemtapp/
COPY . .
RUN pip3 install -r requirements.txt
ENV TZ=Asia/Kolkata
CMD ["gunicorn3", "--bind=0.0.0.0:5000", "wsgi:app", "--workers=3", "worker_class=gthread", "--timeout=900", "--error-logfile=/error.log", "--log-level=DEBUG", "--access-logfile=/access.log", "--capture-output"]