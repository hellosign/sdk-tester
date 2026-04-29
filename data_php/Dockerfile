FROM php:8.3-cli
LABEL maintainer="Dropbox Sign API Team <apisupport@hellosign.com>"

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        unzip \
        libzip-dev && \
    docker-php-ext-install zip && \
    rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

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
