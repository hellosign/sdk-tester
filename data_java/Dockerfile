FROM maven:3-jdk-11
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /test_fixtures && \
    mkdir /tests && \
    mkdir /app && \
    mkdir -p /app/src/main/java/com/hellosign/sdk/

COPY ./pom.xml /app/pom.xml
COPY ./Requester.java /app/src/main/java/com/hellosign/sdk/Requester.java
COPY ./run-dev /app/run-dev

RUN cd /app && \
    mvn -f pom.xml compile assembly:single

WORKDIR /app
VOLUME /file_uploads
VOLUME /app
VOLUME /test_fixtures
VOLUME /tests