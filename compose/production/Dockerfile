FROM python:3.13

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directories
RUN mkdir -p /app /var/log/nginx
WORKDIR /app

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY . /app/

# Install Python deps
RUN poetry install

# Build frontend and collect static
RUN bash scripts/install_tailwind.sh
RUN bash scripts/build.sh
RUN poetry run python manage.py collectstatic --noinput

# Copy and prepare Celery scripts
COPY ./compose/production/celery/worker/start /start-celeryworker
COPY ./compose/production/celery/beat/start /start-celerybeat
COPY ./compose/production/celery/flower/start /start-flower
RUN chmod +x /start-celeryworker /start-celerybeat /start-flower && \
    sed -i 's/\r$//g' /start-celery*

# Configure Nginx to reverse proxy to Gunicorn and serve /media
RUN rm /etc/nginx/sites-enabled/default
RUN echo '\
server {\n\
    listen 8000;\n\
\n\
    location /media/ {\n\
        alias /app/media/;\n\
        autoindex on;\n\
    }\n\

    location / {\n\
        proxy_pass http://127.0.0.1:9000;\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
        proxy_set_header X-Forwarded-Proto $scheme;\n\
    }\n\
}' > /etc/nginx/sites-enabled/app.conf

# Expose Nginx port
EXPOSE 8000

# Start both Gunicorn and Nginx on container start
CMD bash -c "\
    poetry run gunicorn core.wsgi:application --bind 127.0.0.1:9000 --workers 3 & \
    nginx -g 'daemon off;'"
