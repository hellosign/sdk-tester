FROM node:17
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /app

COPY ./.npmrc /app/.npmrc
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json
COPY ./requester.ts /app/requester.ts
COPY ./tsconfig.json /app/tsconfig.json

RUN git clone https://github.com/HelloFax/hellosign-nodejs-sdk.git /app/src && \
    cd /app/src && \
    git checkout openapi && \
    git submodule init && \
    git submodule update && \
    npm install && \
    npm run build && \
    npm pack && \
    mv hellosign-sdk-*.tgz /app/hellosign-sdk.tgz && \
    cd /app && \
    npm install && \
    npm run build

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
