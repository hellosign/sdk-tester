FROM python:3.10-buster
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    git clone https://github.com/hellosign/hellosign-python-sdk.git /app && \
    cd /app && \
    git checkout openapi && \
    git submodule init && \
    git submodule update && \
    pip install -r requirements.txt

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
