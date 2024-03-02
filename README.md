## Example FastAPI backend with distributed task queue

### Prerequisites
- Install **docker** and **docker-compose** - https://docs.docker.com/compose/install/
<br> Verify installation by issuing `docker --version` and `docker-compose --version` in the terminal
- Install **justfile** support - https://github.com/casey/just (**brew** package manager handles this well)

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
`<docker_container_ip>:8080/docs`.
The link can be obtained by issuing `just api-link`

### justfile
**justfile** contains simple command automations that make local development easier. You can, for
example:
- check logs of specified container
- display running containers
- access db container to issue queries directly in SQL
- run tests with `just test`. If integration tests fail, just wait half a minute before running them again,
app needs time to acquire all connections
Complete list of actions can be viewed after typing `just` in the terminal


### Local development
- install **pyenv** - https://github.com/pyenv/pyenv
- create virtual environment with python version specified in **server/Dockerfile**
```commandline
pyenv install 3.11.2
pyenv virtualenv 3.11.2 xberry
pyenv activate xberry
pyenv local xberry
```
Last command will create **.python-version** file in the project root, which will
automatically activate the virtual environment when you navigate to the project root.
- Navigate to project root and issue `just dev-env` to install packages and `pre-commit` hooks
- Use `just pre-commit` to run linters manually and compile **requirements.txt** file
from **requirements.in** file

#### Local tests
Tests can be run on local instance of the application. To do so, you need to:
- run `just stop-api`
- run `just echo-ip` and copy the output to `/server/.env.local` file
- run `entrypoints.fastapi_app` in your IDE with **.env.local** file as environment variables
- run tests either via `pytest` command or via IDE with **.env.local** file as environment variables


### Task monitor
Application uses flower as task monitor. The link can and credentials can be obtained by issuing
`just flower-link` command.
