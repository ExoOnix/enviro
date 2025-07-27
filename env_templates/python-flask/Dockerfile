FROM ghcr.io/exoonix/enviro_dockerenv:latest

USER coder

RUN python3 -m venv /home/coder/project/.venv

RUN /home/coder/project/.venv/bin/pip install --upgrade pip && \
    /home/coder/project/.venv/bin/pip install flask

ENV VIRTUAL_ENV=/home/coder/project/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --chown=coder:coder ./main.py /home/coder/project/main.py
