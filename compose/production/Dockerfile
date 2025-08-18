FROM python:3.13-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directories
RUN mkdir -p /app /var/log/nginx
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies (cached if pyproject/poetry.lock unchanged)
RUN poetry install --no-root

# Copy the rest of the application
COPY . /app/

# Build frontend and collect static files
RUN bash scripts/install_tailwind.sh && \
    bash scripts/build.sh && \
    poetry run python manage.py collectstatic --noinput

# Prepare Celery scripts
COPY ./compose/production/celery/worker/start /start-celeryworker
COPY ./compose/production/celery/beat/start /start-celerybeat
COPY ./compose/production/celery/flower/start /start-flower
RUN chmod +x /start-celeryworker /start-celerybeat /start-flower && \
    sed -i 's/\r$//g' /start-celery*

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
RUN echo '\
    server {\n\
    listen 8000;\n\
    \n\
    location /media/ {\n\
    alias /app/media/;\n\
    autoindex on;\n\
    }\n\
    \n\
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

# Start Gunicorn and Nginx
CMD bash -c "\
    poetry run gunicorn core.wsgi:application --bind 127.0.0.1:9000 --workers 3 & \
    nginx -g 'daemon off;'"
