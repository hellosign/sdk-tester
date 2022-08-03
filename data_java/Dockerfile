FROM maven:3-jdk-11
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /app && \
    mkdir -p /app/src/main/java/com/hellosign/sdk/

COPY ./pom.xml /app/pom.xml
COPY ./Requester.java /app/src/main/java/com/hellosign/sdk/Requester.java

RUN cd /app && \
    mvn -f pom.xml compile assembly:single

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
