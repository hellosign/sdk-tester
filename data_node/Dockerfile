FROM node:17
LABEL maintainer="Dropbox Sign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /test_fixtures && \
    mkdir /tests && \
    mkdir /app

COPY ./package.json /app/package.json
COPY ./requester.ts /app/requester.ts
COPY ./tsconfig.json /app/tsconfig.json

RUN cd /app && \
    npm install && \
    npm run build

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
VOLUME /test_fixtures
VOLUME /tests
