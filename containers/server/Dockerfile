# pull official base image
FROM python:3.10-slim

WORKDIR /var/teenwork

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN pip install --upgrade pip pipenv
COPY ./backend/Pipfile ./backend/Pipfile.lock ./

RUN pipenv install --dev --deploy --system
# RUN PIP_IGNORE_INSTALLED=1 pipenv sync --system

# copy project
COPY . .
