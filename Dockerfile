FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git python3-pip ffmpeg -y

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

CMD python3 bot.py
