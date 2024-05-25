FROM ubuntu:focal

WORKDIR /admin
COPY . .

RUN apt update -y
RUN apt upgrade -y

# Set timezone (With the Daylight saving schedule)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install tzdata
ENV TZ=Europe/Prague
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt install python3 python3-pip -y
RUN pip3 install -r ./requirements.txt

RUN sed -i 's/from __main__ import socketio/from app import socketio/g' ./app/web/blueprints/b_socketio.py

EXPOSE 8000