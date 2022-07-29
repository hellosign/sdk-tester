FROM ruby:3.1
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /app

COPY ./Gemfile /app/Gemfile
COPY ./requester.rb /app/requester.rb

RUN cd /app && \
    bundle install

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
