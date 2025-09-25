FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER coder

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

RUN code-server --install-extension rust-lang.rust-analyzer


RUN wget https://github.com/vadimcn/codelldb/releases/download/v1.11.5/codelldb-linux-x64.vsix && \
    code-server --install-extension codelldb-linux-x64.vsix && \
    rm codelldb-linux-x64.vsix


COPY --chown=coder:coder ./vscode/settings.json /home/coder/.local/share/code-server/User/settings.json
COPY --chown=coder:coder ./vscode/launch.json /home/coder/project/.vscode/launch.json

WORKDIR /home/coder/project

RUN /home/coder/.cargo/bin/cargo init --bin