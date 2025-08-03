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

RUN npx -y express-generator --view pug

RUN npm install


COPY --chown=coder:coder ./vscode/settings.json /home/coder/.local/share/code-server/User/settings.json
RUN code-server --install-extension formulahendry.code-runner
