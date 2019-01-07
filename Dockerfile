FROM ubuntu:latest
MAINTAINER Austin Graham "austingraham731@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install --upgrade pip

COPY . /src

WORKDIR /src

RUN python3 setup.py install
EXPOSE 80
CMD pserve conf/production.ini
