FROM python:3.10-buster
LABEL maintainer="Dropbox Sign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /test_fixtures && \
    mkdir /tests && \
    mkdir /app

COPY ./requester.py /app/requester.py
COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

RUN cd /app && \
    pip install -r requirements.txt

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
VOLUME /test_fixtures
VOLUME /tests
