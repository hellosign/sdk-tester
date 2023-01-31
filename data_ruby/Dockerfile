FROM ruby:3.1
LABEL maintainer="Dropbox Sign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /test_fixtures && \
    mkdir /tests && \
    mkdir /app

COPY ./Gemfile /app/Gemfile
COPY ./requester.rb /app/requester.rb

RUN cd /app && \
    bundle install

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
VOLUME /test_fixtures
VOLUME /tests
