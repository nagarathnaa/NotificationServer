FROM ubuntu:18.04
MAINTAINER mohan@devopsenabler.com
RUN apt-get update -y && \
    apt-get install -y python3-pip
WORKDIR /opt/docker/doeassessmemtapp/
COPY . .
RUN pip3 install -r requirements.txt
ENV TZ=Asia/Kolkata
CMD [ "python", "./trigger_notification.py" ]