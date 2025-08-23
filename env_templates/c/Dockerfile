FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

RUN apt update && apt install -y clangd clang

USER coder

RUN code-server --install-extension llvm-vs-code-extensions.vscode-clangd
RUN code-server --install-extension formulahendry.code-runner


COPY --chown=coder:coder ./main.c /home/coder/project/main.c
COPY --chown=coder:coder ./Makefile /home/coder/project/Makefile
COPY --chown=coder:coder ./README.md /home/coder/project/README.md

COPY --chown=coder:coder ./vscode/settings.json /home/coder/.local/share/code-server/User/settings.json