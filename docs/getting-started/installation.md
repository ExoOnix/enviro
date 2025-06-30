# Installation Guide

This guide will help you install and set up Onix Enviro on your infrastructure.

## Prerequisites

- **Docker** and **Docker Compose** installed on your server or local machine.
- A supported OS (Linux recommended).
- Basic knowledge of Docker and command-line usage.

## 1. Clone the Repository

```sh
git clone https://github.com/ExoOnix/enviro.git
cd enviro
```

## 2. Configure Environment Variables

Copy the example environment file and edit it to match your configuration:

```sh
cp .env.example .env
# Edit .env with your preferred editor
```

Set values for database, Django secret key, allowed hosts, etc.

## 3. Set Up Docker Network

Create the required Docker network if it doesn't exist:

```sh
docker network create onixenvnet
```

## 4. Start the Services

Run the following command to start all services:

```sh
docker compose -f docker-compose.production.yaml up --build -d
```

## 5. Apply Database Migrations

After the containers are running, apply Django migrations:

```sh
docker compose -f docker-compose.production.yaml exec django-web poetry run python manage.py migrate
```

## 6. Create a Superuser (Optional)

To access the Django admin, create a superuser:

```sh
docker compose -f docker-compose.production.yaml exec django-web poetry run python manage.py createsuperuser
```

## 7. Access the Platform

- Visit `http://localhost:8081` (or your server's IP/domain) in your browser. (Port can be changed in the docker compose)
- Log in or sign up to start using Onix Enviro.

---

For configuration options, see the [configuration options](./configuration.md).
