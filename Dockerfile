# syntax=docker/dockerfile:1
FROM python:3.9.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "bash" ,"main.sh","master", "3000", "MASTER=3000",  "bash", "main.sh", "worker", "3001" ]

