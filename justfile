#!/usr/bin/env bash

set shell := ["bash", "-uc"]

current_dir := justfile_directory()
compose_files := "-f docker-compose.yml"
docker_compose := "docker-compose"
docker_inspect_ip := "docker inspect -f {{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}"
containers_table_format := "table {{.ID}}\t{{.Status}}\t{{.Names}}\t{{.Ports}}"
api_port := "8080"
flower_port := "5555"


default:
    just --list

dev-env:
    pip install -r server/requirements.txt
    pip install -r server/requirements-dev.txt
    pre-commit install

pre-commit:
	pre-commit run --all-files

build:
	docker-compose {{compose_files}} build

up:
	docker-compose {{compose_files}} up -d

down:
	docker-compose down

logs *args='':
	{{docker_compose}} logs {{args}}

api-console:
	docker exec -it api sh

db-console:
	docker exec -it pgdb psql postgres user

stop-api:
    docker stop api

restart-api:
    docker restart api

show-containers:
    docker ps --format "{{containers_table_format}}"

echo-ip:
    #!/usr/bin/env bash
    echo POSTGRES_SERVER=$({{docker_inspect_ip}} pgdb)
    echo FLOWER_SERVER=$({{docker_inspect_ip}} flower)
    echo RABBITMQ_SERVER=$({{docker_inspect_ip}} rabbitmq)
    echo REDIS_SERVER=$({{docker_inspect_ip}} redis)

api-link:
    #!/usr/bin/env bash
    ip=$(echo $({{docker_inspect_ip}} api))
    echo "http://$ip:{{api_port}}/docs"


flower-link:
    #!/usr/bin/env bash
    ip=$(echo $({{docker_inspect_ip}} flower))
    echo "http://$ip:{{flower_port}}"
    echo "username: flower"
    echo "password: mysecretflower"


test: up
	docker-compose run --rm --no-deps --entrypoint=pytest api tests/unit tests/integration
