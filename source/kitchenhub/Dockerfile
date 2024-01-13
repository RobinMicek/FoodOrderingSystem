FROM ubuntu:latest

WORKDIR /kitchenhub
COPY . .

RUN apt update -y
RUN apt upgrade -y

# Set timezone (With the Daylight saving schedule)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install tzdata
ENV TZ=Europe/Prague
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt install python3 python3-pip -y
RUN pip3 install -r ./app/requirements.txt

RUN python3 ./app/database/handle_database.py

CMD ["python3", "./app/web/app.py"]