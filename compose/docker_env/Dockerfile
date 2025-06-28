FROM codercom/code-server:latest

USER root

RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release && \
    mkdir -m 0755 -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-venv python3-pip

RUN usermod -aG docker coder

USER coder

RUN mkdir -p /home/coder/project
RUN mkdir -p /home/coder/logs

RUN code-server --install-extension ms-python.python
RUN code-server --install-extension ms-azuretools.vscode-docker

ENTRYPOINT ["bash"]

CMD ["-c", "sudo rm -f /var/run/docker/containerd/containerd.pid && sudo dockerd > /home/coder/logs/dockerd.log 2>&1 & code-server /home/coder/project --bind-addr 0.0.0.0:8080 --disable-getting-started-override=true --auth=none > /home/coder/logs/code-server.log 2>&1"]