FROM ubuntu:18.04
MAINTAINER mohan@devopsenabler.com
RUN apt-get update -y && \
    apt-get install -y python3-pip gunicorn3
WORKDIR /opt/docker/doeassessmemtapp/
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000