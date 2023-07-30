# pull official base image
FROM python:3.10-slim

WORKDIR /var/teenwork

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /var/teenwork
RUN pip install -r ./requirements.txt
RUN apt-get update && apt-get install -y netcat

# copy project
COPY . .
