FROM ubuntu:latest

WORKDIR /kitchenhub
COPY . .

RUN apt update -y
RUN apt upgrade -y

RUN apt install python3 python3-pip -y

RUN pip3 install -r ./app/requirements.txt

RUN rm ./app/logs.txt

RUN python3 ./app/database/handle_database.py

CMD ["python3", "./app/web/app.py"]