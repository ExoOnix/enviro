FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

# Install Node.js 20
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

# Initialize Next.js app
COPY --chown=coder:coder . /home/coder/project/

RUN npm install