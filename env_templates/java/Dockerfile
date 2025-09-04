FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

RUN apt install -y wget apt-transport-https gpg

RUN wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | tee /etc/apt/trusted.gpg.d/adoptium.gpg > /dev/null

RUN echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list


RUN apt-get update && \
    apt-get install -y temurin-21-jdk maven

USER coder

WORKDIR /home/coder/project

RUN code-server --install-extension EdwinKofler.vscode-hyperupcall-pack-java

COPY --chown=coder:coder ./app /home/coder/project/app

RUN mvn install -f "/home/coder/project/app/pom.xml"