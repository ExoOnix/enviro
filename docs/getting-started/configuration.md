# Configuration

This document explains the environment variables used to configure your Enviro deployment. All variables are set in the `.env` file at the root of your project. You can use `.env.example` as a template.

## Django Settings

- **DJANGO_SECRET_KEY**  
  Secret key for Django. Change this to a unique, unpredictable value in production.

- **DEBUG**  
  Set to `True` for development, `False` for production.

- **DJANGO_LOGLEVEL**  
  Logging level for Django. Common values: `info`, `debug`, `warning`, `error`.

- **DJANGO_ALLOWED_HOSTS**  
  Comma-separated list of hostnames/domain names that this Django site can serve.

## Database Settings

- **DATABASE_ENGINE**  
  Database backend to use. Example: `postgresql_psycopg2`.

- **DATABASE_NAME**  
  Name of the database.

- **DATABASE_USERNAME**  
  Username for the database.

- **DATABASE_PASSWORD**  
  Password for the database user.

- **DATABASE_HOST**  
  Hostname or IP address of the database server.

- **DATABASE_PORT**  
  Port number for the database server.

## Celery Settings

- **CELERY_BROKER_URL**  
  URL for the Celery broker (e.g., Redis).

- **CELERY_RESULT_BACKEND**  
  Backend used by Celery to store task results.

## Environment Preferences

- **ENV_PROVIDER**  
  The environment provider(more coming soon). Options: `docker`.

- **DOCKER_RUNTIME**  
  Docker runtime to use. Example: `default`, you can use `sysbox-runc` if using Sysbox.

- **ENV_IMAGE**  
  Docker image to use for the environment. Example: `codercom/code-server:latest`, if using Sysbox use the docker image `ghcr.io/exoonix/enviro_dockerenv:latest`.

- **ENV_LIMITS**  
  Maximum number of environments a user can create. Set to `0` to disable the limit.

## Reverse Proxy Config

- **HOSTNAME**
  Set to the hostname of your application, for example: `onixtech.org`, only needed if using subdomain routing in `ROUTING_TYPE`.

- **ROUTING_TYPE**
  Set routing type. if using subpath, environments will be placed on /environments/<id>. If using subdomain, environments will be placed on env-<id>.example.com. You need `HOSTNAME` to be set. Options: `subpath`, `subdomain`.

## Email Settings

- **EMAIL_BACKEND** Django email backend.  
    - For console: `django.core.mail.backends.console.EmailBackend`  
    - For SMTP: `django.core.mail.backends.smtp.EmailBackend`

- **EMAIL_HOST**  
  SMTP server host.

- **EMAIL_PORT**  
  SMTP server port. Default for SSL is `465`.

- **EMAIL_USE_TLS**  
  Set to `True` to use TLS.

- **EMAIL_USE_SSL**  
  Set to `True` to use SSL.

- **EMAIL_HOST_USER**  
  SMTP username.

- **EMAIL_HOST_PASSWORD**  
  SMTP password.

---

## Exporting Environment Templates to a Fixture

To export fixtures run:
```sh
./cli poetry run python manage.py dumpdata env_manager.EnvironmentTemplate --indent 2 > apps/env_manager/fixtures/templates.json
```

**Note:**  
After editing your `.env` file, restart your application for changes to take effect.