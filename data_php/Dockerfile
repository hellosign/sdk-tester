FROM jtreminio/php-cli:7.4
LABEL maintainer="Dropbox Sign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /test_fixtures && \
    mkdir /tests && \
    mkdir /app

COPY ./composer.json /app/composer.json
COPY ./requester.php /app/requester.php

RUN cd /app && \
    composer install

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
VOLUME /test_fixtures
VOLUME /tests
