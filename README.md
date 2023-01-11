## Example FastAPI backend with asynchronous database access

### Prerequisites
- Install docker and docker-compose - https://docs.docker.com/compose/install/
- Install **justfile** support - https://github.com/casey/just

### Quickstart
- Navigate to project root and issue following commands
```
just build
just up
```
In case of trouble with **justfile** installation, it's also possible to both build and run
the project with only docker:
```
docker-compose up --build
```
The application with interactive API documentation will be available at
`http://localhost:8080/docs`.

### justfile
**justfile** contains simple command automations that make local development easier. You can, for
example:
- check logs of specified container
- display running containers
- access db container to issue queries directly in SQL
Complete list of actions can be viewed after typing `just` in the terminal
