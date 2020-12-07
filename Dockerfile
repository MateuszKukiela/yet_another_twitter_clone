#FROM python:3.9
#ENV PYTHONUNBUFFERED=1
#WORKDIR /app
#COPY requirements.txt /app/
#RUN pip install -r requirements.txt
#COPY . /app/
# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add python3-dev gcc libc-dev \
    && apk add postgresql-dev \
    && pip install psycopg2

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
#CMD gunicorn web.wsgi:application --bind 0.0.0.0:$PORT
