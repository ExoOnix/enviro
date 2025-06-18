# enviro

Make sure to create the `traefiknet` network with docker

```
docker compose -f docker-compose.production.yaml up --build -d

docker compose -f docker-compose.production.yaml down
```