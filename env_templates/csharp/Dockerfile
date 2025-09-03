FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb &&
    dpkg -i packages-microsoft-prod.deb &&
    rm packages-microsoft-prod.deb

RUN apt-get update && 
    apt-get install -y dotnet-sdk-9.0

USER coder

RUN code-server --install-extension muhammad-sammy.csharp

RUN dotnet new console
