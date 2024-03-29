FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade --force-reinstall pip

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2 \
    && pip3 install django-extensions \
    && pip3 install django-widget-tweaks \
    && apt-get -y install xmlsec1 

RUN pip3 install -r requirements.txt

COPY . /app/