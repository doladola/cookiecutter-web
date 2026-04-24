# Copilot Instructions

## Build, test, and lint commands

- This repository is a Cookiecutter template. The normal smoke test for template changes is generating a project from the repo root:
  - `uvx cookiecutter -f .`
- In a generated project, local dependencies are started with:
  - `cp .env.example .env`
  - `docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d`
- Common generated-project Django commands run through `uv`:
  - `uv run manage.py startapp <app_name>`
  - `uv run manage.py makemigrations`
  - `uv run manage.py migrate`
  - `uv run manage.py runserver`
- Test commands for a generated project:
  - Full suite: `uv run manage.py test`
  - Single test: `uv run manage.py test myapp.tests.SomeTestCase.test_method`
- Production-oriented helper commands in a generated project:
  - `./cmd.sh dev up`
  - `./cmd.sh dev down`
  - `./cmd.sh build`
  - `./cmd.sh run`
  - `./cmd.sh stop`
- No dedicated lint configuration is checked into this template repository.

## High-level architecture

- Root-level files define the scaffold itself:
  - `cookiecutter.json` declares prompts, defaults, and feature flags.
  - `hooks/pre_gen_project.py` validates input before generation.
  - `hooks/post_gen_project.py` mutates the generated project after generation.
- `{{ cookiecutter.project }}` is the template for the generated Django project. Files under this tree are not a live app in this repository; they are copied with Jinja substitutions and conditionals applied.
- The generated project starts as a minimal Django project (`manage.py`, `{{ cookiecutter.project }}/settings.py`, `urls.py`, `wsgi.py`, `asgi.py`) plus deployment assets (`docker/`, `Dockerfile`, `entrypoint.sh`, `cmd.sh`, env examples, generated README).
- Optional capabilities are split across template conditionals and post-generation dependency installation:
  - Redis and Celery are treated as built-in defaults: the generated project always includes their dependencies and base wiring.
  - Sentry is conditionally imported and initialized in `settings.py`.
  - Django Ninja is installed by the post-generation hook and documented in the generated README.
- Deployment is Docker-first:
  - `docker/docker-compose.dev.yaml` provides local Postgres and Redis for development.
  - `docker/docker-compose.prd.yaml` defines the project-local Nginx, Django web container, database, Redis, and Celery services.
  - `docker/nginx/` contains the outer Nginx example used to route multiple projects by path prefix.
  - `entrypoint.sh` performs migrations, `collectstatic`, and superuser provisioning before starting Gunicorn.

## Key conventions

- Treat `{{ cookiecutter.project }}/README.md` as shipped product documentation. If template commands, env files, feature flags, or deployment flow change, update that README with the code changes.
- Feature flags are cross-cutting. Changes to user-facing flags like `use_ninja` or `use_sentry`, or to the internal always-on Redis/Celery wiring, usually require coordinated edits in:
  - `cookiecutter.json`
  - `hooks/pre_gen_project.py`
  - `hooks/post_gen_project.py`
  - Jinja-conditional template files under `{{ cookiecutter.project }}`
  - Generated-project README examples
- Redis and Celery are no longer user-facing feature flags; treat their settings, dependencies, and Celery app wiring as always-on parts of the generated project.
- Dependencies are intentionally added after generation with `uv add --link-mode=copy` in `hooks/post_gen_project.py`; `pyproject.toml` is only a minimal starting point.
- Environment configuration is split by runtime:
  - `{{ cookiecutter.project }}\.env.example` is the generated project's root env template used for local development and direct Django commands.
  - `{{ cookiecutter.project }}\docker\.env.example` is the container/deployment env template used by production-oriented Docker flows.
- The generated settings expect env-driven paths and host configuration (`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `FORCE_SCRIPT_NAME`, `LOGFILE`, database/Redis hosts). Keep env examples, settings, compose files, and deployment docs aligned when changing those values.
