## Example FastAPI backend with asynchronous queue

### Prerequisites
- Install **docker** and **docker-compose** - https://docs.docker.com/compose/install/
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


### Local development
- install **pyenv** - https://github.com/pyenv/pyenv
- create virtual environment with python version specified in **server/Dockerfile**
```commandline
pyenv install 3.11.2
pyenv virtualenv 3.11.2 my_venv
pyenv activate my_venv
pyenv local my_venv
```
Last command will create **.python-version** file in the project root, which will
automatically activate the virtual environment when you navigate to the project root.
- Navigate to project root and issue `just dev-env` to install packages and `pre-commit` hooks
- Use `just pre-commit` to run linters manually and compile **requirements.txt** file
from **requirements.in** file
