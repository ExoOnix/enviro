FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/coder/project

USER coder

RUN code-server --install-extension formulahendry.code-runner

COPY --chown=coder:coder ./index.js /home/coder/project/index.js
