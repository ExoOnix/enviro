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


USER coder

RUN npm init -y

RUN npm install express

COPY --chown=coder:coder ./index.js /home/coder/project/index.js

RUN code-server --install-extension formulahendry.code-runner