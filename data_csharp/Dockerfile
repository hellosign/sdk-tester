FROM mcr.microsoft.com/dotnet/sdk:6.0
LABEL maintainer="HelloSign API Team <apisupport@hellosign.com>"

USER root

RUN mkdir /file_uploads && \
    mkdir /test_fixtures && \
    mkdir /tests && \
    mkdir /app

COPY ./Program.cs /app/Program.cs

RUN cd /app && \
    git clone https://github.com/hellosign/hellosign-dotnet-sdk.git && \
    cd hellosign-dotnet-sdk/ && \
    git checkout openapi && \
    git submodule update --init --recursive --remote && \
    dotnet new console -o sdk-tester && \
    mv /app/Program.cs sdk-tester && \
    dotnet add sdk-tester/sdk-tester.csproj reference src/HelloSign/HelloSign.csproj && \
    dotnet build


WORKDIR /app
VOLUME /file_uploads
VOLUME /app
VOLUME /test_fixtures
VOLUME /tests
