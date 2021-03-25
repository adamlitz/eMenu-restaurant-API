# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/emenu_backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install necessary dependencies
RUN apk update && apk add \
    musl-dev gcc python3-dev postgresql-dev postgresql-client \
    libxml2-dev libxslt-dev libressl-dev libffi-dev openssl-dev \
    jpeg-dev zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --default-timeout=1000 -r requirements.txt

# copy project
COPY . .

RUN chmod +x ./wait_for_postgres.sh
