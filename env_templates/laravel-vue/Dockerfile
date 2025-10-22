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


# Add PHP 8.4 repository
RUN curl -fsSL https://packages.sury.org/php/README.txt | bash - \
    && apt-get update \
    && apt-get install -y \
    openssl php8.4 php8.4-bcmath php8.4-curl php8.4-mbstring php8.4-mysql php8.4-tokenizer php8.4-xml php8.4-zip php8.4-sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install Composer globally
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /home/coder/project

USER coder

RUN code-server --install-extension laravel.vscode-laravel
RUN code-server --install-extension bmewburn.vscode-intelephense-client
RUN code-server --install-extension Vue.volar

# Initialize Next.js app
COPY --chown=coder:coder . /home/coder/project/

RUN npm install

RUN composer install

RUN composer run setup
