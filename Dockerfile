FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2 \
    && pip3 install django-extensions \
    && pip3 install django-widget-tweaks

RUN pip3 install -r requirements.txt

COPY . /app/