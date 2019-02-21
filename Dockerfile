FROM ubuntu:latest
MAINTAINER Austin Graham "austingraham731@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libffi-dev
RUN rm -rf /usr/lib/python3/dist-packages/setuptools*
RUN pip3 install --upgrade pip
RUN pip3 install setuptools

COPY . /src

WORKDIR /src

RUN python3 setup.py install
EXPOSE 80
CMD pserve conf/production.ini
