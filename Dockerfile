FROM python:3.9.6-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git curl python3-pip ffmpeg python3-dev default-libmysqlclient-dev  build-essential libssl-dev -y 
RUN python3.9 -m pip install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
ENV URLDB="mysql-url"
RUN python3.9 -m pip install -U -r requirements.txt
CMD python3.9 main.py
