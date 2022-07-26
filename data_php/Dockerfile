FROM jtreminio/php-cli:7.4
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    git clone https://github.com/hellosign/hellosign-php-sdk.git /app && \
    cd /app && \
    git checkout openapi && \
    git submodule init && \
    git submodule update && \
    composer install

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
