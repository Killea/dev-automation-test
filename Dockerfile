FROM jenkins/jenkins:lts
USER root
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install  mysql-client python3 python3-pip -y
RUN apt-get install default-libmysqlclient-dev -y
RUN pip3 install mysqlclient
