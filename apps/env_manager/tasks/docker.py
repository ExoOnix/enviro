import docker
from ..models import Environment
from core.celery import app

from django.conf import settings

@app.task
def create_container(environment_id):
    
    client = docker.from_env()

    container = None
    try:
        environment = Environment.objects.get(id=environment_id)
        env_id = environment.id
        router_name = f"code-server-{env_id}"
        service_name = f"code-server-{env_id}"
        middleware_stripprefix = f"code-server-stripprefix-{env_id}"
        middleware_forwardauth = f"code-server-forwardauth-{env_id}"

        routing_type = settings.ROUTING_TYPE
        if routing_type == "subpath":
            path_prefix = f"/environment/{env_id}"
            labels = {
                "traefik.enable": "true",
                f"traefik.http.routers.{router_name}.rule": f"PathPrefix(`{path_prefix}`)",
                f"traefik.http.routers.{router_name}.entrypoints": "web",
                f"traefik.http.routers.{router_name}.service": service_name,
                f"traefik.http.services.{service_name}.loadbalancer.server.port": "23000",
                f"traefik.http.middlewares.{middleware_stripprefix}.stripprefix.prefixes": path_prefix,
                f"traefik.http.routers.{router_name}.middlewares": f"{middleware_forwardauth},{middleware_stripprefix}",
                f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.address": "http://django-docker:8000/auth/",
                f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.trustForwardHeader": "true",
                f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.authResponseHeaders": "Remote-User"
            }
        elif routing_type == "subdomain":
            subdomain = f"env-{env_id}.{settings.HOSTNAME}"
            labels = {
                "traefik.enable": "true",
                f"traefik.http.routers.{router_name}.rule": f"Host(`{subdomain}`)",
                f"traefik.http.routers.{router_name}.entrypoints": "web",
                f"traefik.http.routers.{router_name}.service": service_name,
                f"traefik.http.services.{service_name}.loadbalancer.server.port": "23000",
                f"traefik.http.routers.{router_name}.middlewares": f"{middleware_forwardauth}",
                f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.address": "http://django-docker:8000/auth/",
                f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.trustForwardHeader": "true",
                f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.authResponseHeaders": "Remote-User"
            }
        run_kwargs = dict(
            image=environment.image,
            labels=labels,
            network="onixenvnet",
            restart_policy={"Name": "unless-stopped"},
            detach=True
        )
        # Only set command and entrypoint if using codercom/code-server:latest
        if environment.image == "codercom/code-server:latest":
            run_kwargs["command"] = [
                "-c",
                "mkdir -p /home/coder/project && code-server /home/coder/project --bind-addr 0.0.0.0:23000 --disable-getting-started-override=true --auth=none"
            ]
            run_kwargs["entrypoint"] = "bash"
        if settings.DOCKER_RUNTIME != "default":
            run_kwargs["runtime"] = settings.DOCKER_RUNTIME

        container = client.containers.run(**run_kwargs)
        
        environment.resource_id = container.id
        environment.status = "running"
        environment.save()
        print(f"Container {container.name} started with ID {container.id}")
    except Exception as e:
        if container:
            container.remove(force=True)
        environment.delete()
        raise e

@app.task
def delete_container(environment_id):
    client = docker.from_env()
    try:
        environment = Environment.objects.get(id=environment_id)
        container = client.containers.get(environment.resource_id)
        
        try:
            if container.status == 'running':
                container.kill()
            container.remove()
            environment.delete()
        except Exception as e:
            print(f"Error removing environment: {e}")
            raise e
    except docker.errors.NotFound:
        print(f"Container with id {environment.resource_id} not found, removing Environment record.")
        environment.delete()
    except Exception as e:
        raise e

@app.task
def stop_container(environment_id):
    client = docker.from_env()
    try:
        environment = Environment.objects.get(id=environment_id)
        container = client.containers.get(environment.resource_id)
        
        environment.status = "stopped"
        environment.save()
        
        container.stop()
    except Exception as e:
        raise e
    
@app.task
def start_container(environment_id):
    client = docker.from_env()
    try:
        environment = Environment.objects.get(id=environment_id)
        container = client.containers.get(environment.resource_id)
        
        environment.status = "running"
        environment.save()
        
        container.start()
    except Exception as e:
        raise e