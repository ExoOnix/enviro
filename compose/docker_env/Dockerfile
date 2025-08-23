FROM golang:1.25.0 AS proxy_builder

WORKDIR /app

COPY ./port_proxy .

RUN go build

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

# PROXY
COPY --from=proxy_builder /app/port_proxy /usr/lib/enviro-subpath-proxy/bin/port_proxy

RUN code-server --install-extension ms-python.python
RUN code-server --install-extension ms-azuretools.vscode-docker

HEALTHCHECK --interval=30s --timeout=5s --start-period=3s --retries=3 \
    CMD curl -fsSL http://localhost:23000/healthz || exit 1


ENTRYPOINT ["bash"]

EXPOSE 23000
EXPOSE 23001

CMD ["-c", "sudo rm -f /var/run/docker/containerd/containerd.pid && \
    sudo rm -f /var/run/docker.pid && \
    sudo dockerd > /home/coder/logs/dockerd.log 2>&1 & \
    /usr/lib/enviro-subpath-proxy/bin/port_proxy > /home/coder/logs/port_proxy.log 2>&1 & \
    code-server /home/coder/project --bind-addr 0.0.0.0:23000 --disable-getting-started-override=true --auth=none > /home/coder/logs/code-server.log 2>&1"]
