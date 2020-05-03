FROM ubuntu:18.04

MAINTAINER chirag_asawa

RUN apt-get update && apt-get upgrade
 
RUN apt-get install python3 -y 

RUN apt-get install python3-pip -y

WORKDIR /root/

ADD project.tar .

ENV LC_ALL=C.UTF-8

ENV LANG=C.UTF-8

WORKDIR /root/project

RUN pip3 install pipenv

RUN pipenv install --system --deploy --ignore-pipfile
 
ENV FLASK_APP conftest.py

EXPOSE 80

CMD ["flask","run","-h","0.0.0.0","-p","80"]





