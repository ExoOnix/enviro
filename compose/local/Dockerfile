FROM python:3.13

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    watchman \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directory
RUN mkdir -p /app /var/log/nginx
WORKDIR /app

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY . /app/

# Install Python dependencies
RUN poetry install

# Prepare Celery scripts
COPY ./compose/local/celery/worker/start /start-celeryworker
COPY ./compose/local/celery/beat/start /start-celerybeat
COPY ./compose/local/celery/flower/start /start-flower
RUN chmod +x /start-celeryworker /start-celerybeat /start-flower && \
    sed -i 's/\r$//g' /start-celery*

# Configure Nginx to listen on port 8000 and proxy to Django on 8001
RUN rm /etc/nginx/sites-enabled/default
RUN echo '\
    server {\n\
    listen 8000;\n\
    \n\
    client_max_body_size 50M;\n\
    \n\
    \n\
    location /media/ {\n\
    alias /app/media/;\n\
    autoindex on;\n\
    }\n\

    location / {\n\
    proxy_pass http://127.0.0.1:8001;\n\
    proxy_set_header Host $host;\n\
    proxy_set_header X-Real-IP $remote_addr;\n\
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
    proxy_set_header X-Forwarded-Proto $scheme;\n\
    }\n\
    }' > /etc/nginx/sites-enabled/app.conf

# Expose port 8000 (Nginx will handle it)
EXPOSE 8000

# Start Django dev server + Nginx
CMD bash -c "\
    poetry run python manage.py runserver 127.0.0.1:8001 & \
    nginx -g 'daemon off;'"
