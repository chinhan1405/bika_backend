# Installing project for developing on local PC

You have to have the following tools installed prior initializing the project:

- [docker](https://docs.docker.com/engine/installation/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [poetry](https://python-poetry.org/docs/#installation)

## Backend

### Task runner

For easier running of everyday tasks, like:

- run dev server
- run all tests
- run linters
- run celery workers
- ...

We use [invoke](https://pypi.org/project/invoke/).

It provides shortcuts for most of the tasks, so it's like collection of bash scrips
or makefile or `npm scripts`.

To enable autocompletion of invoke commands add this line to your `~/.zshrc`

```bash
source <(inv --print-completion-script zsh)
```

### Python interpreter

Also `invoke` abstract "python interpreter", so you can use both `virtual env`
and `dockerized` python interpreter for working with project
(see `tasks.py` file).

- `virtualenv` is the default approach that requires python interpreter,
virtualenv, etc.
- `dockerized` is simpler for quick starting project and for experienced
developers

Suggested approach is using `virtualenv`

### Services

Project may use external services like Database (postgres), message broker,
cache (redis). For easier set up they are defined in `compose.yaml` file,
and they are automatically prepared / started when using `invoke`.

### Prepare python env

Create separate python virtual environment if you are going to run it in
local:

```bash
poetry config virtualenvs.in-project true
uv venv --python 3.12 --prompt bika --seed
source .venv/bin/activate && poetry install
```

Set up aliases for docker hosts in `/etc/hosts`:

```text
127.0.0.1 postgres
127.0.0.1 redis
127.0.0.1 mailpit
127.0.0.1 s3.minio.localhost
```

Start project initialization that will set up docker containers,
python/system env:

```bash
inv project.init
```

Run the project and go to `localhost:8000` page in browser to check whether
it was started:

```bash
inv django.run
```

That's it. After these steps, the project will be successfully set up.

Once you run `project.init` initially you can start web server with
`inv django.run` command without executing `project.init` call.

## Frontend

You can run frontend application for debugging or testing by simply using
`inv frontend.run`. This command clones frontend repository and puts it in the
parent dir, then installs node packages and runs application. Please, ensure you
installed [volta](https://docs.volta.sh/guide/getting-started) to manage node versions.

**Note**: You can change link/path to frontend app repository in
[invocations/frontend.py](../invocations/frontend.py).

## Devops tools

You will need:

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [teleport](https://goteleport.com/docs/getting-started/)
- [pack-cli](https://buildpacks.io/docs/tools/pack/)

Most of needed shortcuts can be called via invoke `inv k8s.###`.

Before run commands log in and set context:

```bash
inv k8s.login
inv k8s.set-context
```

See other useful commands for k8s:

```bash
inv -l k8s
```
