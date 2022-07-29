FROM jtreminio/php-cli:7.4
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /app

COPY ./composer.json /app/composer.json
COPY ./requester.php /app/requester.php

RUN cd /app && \
    composer install

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
