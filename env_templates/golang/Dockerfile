FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER root

RUN wget https://go.dev/dl/go1.25.0.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.25.0.linux-amd64.tar.gz
RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
RUN rm -f go1.25.0.linux-amd64.tar.gz

USER coder

RUN code-server --install-extension formulahendry.code-runner
RUN code-server --install-extension golang.Go

COPY --chown=coder:coder ./main.go /home/coder/project/main.go
