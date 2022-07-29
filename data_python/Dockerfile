FROM python:3.10-buster
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /app

COPY ./requester.py /app/requester.py
COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

RUN cd /app && \
    pip install -r requirements.txt

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
