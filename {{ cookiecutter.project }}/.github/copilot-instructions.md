# 项目说明

这是一个由 `cookiecutter-web` 生成的固定技术栈 Django 项目，默认包含 Django、PostgreSQL、Redis、Celery、HTMX、Alpine.js、Tailwind CSS（开发期 CDN）、Docker、Nginx 和 Sentry。

## 默认工作方式

- 优先在 **devcontainer** 中打开项目，再运行 Copilot CLI。
- 项目运行依赖 Docker Compose；不要假设宿主机虚拟环境是默认路径。
- 高价值入口命令优先使用：
  - `./cmd.sh dev up`
  - `./cmd.sh dev down`
  - `./cmd.sh dev logs`
  - `./cmd.sh verify`

## 关键约定

- `core` 中的 starter demo 是模板自带的验证表面，用来帮助确认 PostgreSQL、Redis、Celery 和基础页面流程是否连通。
- 更深入的依赖验证走 Django tests 和 `python manage.py verify_stack`，不要把 demo 代码扩展成业务逻辑。
- 修改环境配置时，同步检查 `.env.example`、`docker/docker-compose.dev.yaml`、`docker/docker-compose.prd.yaml`、README 和 `settings.py`。
- 如果只是验证模板是否可用，优先运行模板仓库里的 `python tools/validate_template.py`；如果是在生成项目里验证栈连通性，优先运行 `./cmd.sh verify`。
