#!/usr/bin/env bash

set shell := ["bash", "-uc"]

current_dir := justfile_directory()
compose_files := "-f docker-compose.yml"
docker_compose := "docker-compose"
docker_inspect_ip := "docker inspect -f {{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}"
containers_table_format := "table {{.ID}}\t{{.Status}}\t{{.Names}}\t{{.Ports}}"


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

echo-postgres-ip:
    #!/usr/bin/env bash
    echo POSTGRES_SERVER=$({{docker_inspect_ip}} pgdb)
