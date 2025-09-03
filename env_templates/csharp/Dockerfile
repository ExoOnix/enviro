FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    sudo dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb

RUN apt-get update && \
    apt-get install -y dotnet-sdk-9.0

USER coder


COPY --chown=coder:coder ./vscode/settings.json /home/coder/.local/share/code-server/User/settings.json

RUN code-server --install-extension muhammad-sammy.csharp
RUN code-server --install-extension formulahendry.code-runner
RUN code-server --install-extension jsw.csharpextensions

WORKDIR /home/coder/project

RUN dotnet new console --use-program-main
