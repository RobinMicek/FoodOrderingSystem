FROM ubuntu:latest

WORKDIR /admin
COPY . .

RUN apt update -y
RUN apt upgrade -y

RUN apt install python3 python3-pip -y

RUN pip3 install -r ./requirements.txt

RUN rm ./app/logs.txt

RUN sed -i 's/from __main__ import socketio/from app import socketio/g' ./app/web/blueprints/b_socketio.py

EXPOSE 8000