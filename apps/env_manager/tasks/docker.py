import docker
from ..models import Environment
from core.celery import app
import uuid
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
        network_name = f"enviro_envnet-{env_id}"
        container_name = f"code-server-{env_id}-{uuid.uuid4().hex[:6]}"
        middleware_stripprefix = f"code-server-stripprefix-{env_id}"
        middleware_forwardauth = f"code-server-forwardauth-{env_id}"
        traefik_container_name = "traefik"
        
        try:
            network = client.networks.get(network_name)
            print(f"Network {network_name} already exists.")
        except docker.errors.NotFound:
            network = client.networks.create(network_name, driver="bridge", check_duplicate=True)
            print(f"Created network {network_name}")
            
        traefik_container = client.containers.get(traefik_container_name)
        connected_networks = traefik_container.attrs["NetworkSettings"]["Networks"]
        if network_name not in connected_networks:
            network.connect(traefik_container)
            
            
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
            name=container_name,
            image=environment.image,
            labels=labels,
            network=network_name,
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
        traefik_container_name = "traefik"
        
        try:
            if container.status == 'running':
                container.kill()
            container.remove()
            # Delete network if it exists
            env_id = environment.id
            network_name = f"enviro_envnet-{env_id}"
            traefik_container = client.containers.get(traefik_container_name)
            
            network = client.networks.get(network_name)
            connected_networks = traefik_container.attrs["NetworkSettings"]["Networks"]
            if network_name in connected_networks:
                network.disconnect(traefik_container, force=True)
                print(f"Disconnected {traefik_container_name} from network {network_name}")
            network.remove()
            
            environment.delete()
        except Exception as e:
            print(f"Error removing environment: {e}")
            raise e
    except docker.errors.NotFound:
        print(f"Container with id {environment.resource_id} not found, removing Environment record.")
        try:
            traefik_container_name = "traefik"
            env_id = environment.id
            network_name = f"enviro_envnet-{env_id}"
            traefik_container = client.containers.get(traefik_container_name)
            
            network = client.networks.get(network_name)
            connected_networks = traefik_container.attrs["NetworkSettings"]["Networks"]
            if network_name in connected_networks:
                network.disconnect(traefik_container, force=True)
                print(f"Disconnected {traefik_container_name} from network {network_name}")
            network.remove()
        except Exception as e:
            print(f"Error removing network: {e}")
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