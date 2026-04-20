# 项目说明

这是一个 **固定技术栈的 Cookiecutter Django 模板仓库**。模板不再通过开关组合不同栈，而是始终生成同一种项目：

- Django
- PostgreSQL
- Redis
- Celery + django-celery-beat
- HTMX + Alpine.js
- Tailwind CSS（开发期 CDN）
- Docker
- Nginx（生产环境）
- Sentry

生成项目默认 **Linux-only**，并采用 **Docker-only 开发模式**。

## 常用命令

### 模板仓库

```sh
# 渲染模板
uvx cookiecutter -f cookiecutter-web/

# 校验模板
python tools/validate_template.py
```

### 生成后的 Django 项目

```sh
# 初始化 .env（也可省略；dev/prod/manage/test 会自动补齐）
./cmd.sh bootstrap

# 启动开发环境
./cmd.sh dev up

# 停止开发环境
./cmd.sh dev down

# 查看日志
./cmd.sh dev logs

# 执行 Django 管理命令
./cmd.sh manage migrate
./cmd.sh manage createsuperuser

# 运行测试
./cmd.sh test

# 启动生产编排
./cmd.sh prod up
./cmd.sh prod down
```

仓库中 **没有单独配置 lint / format / type-check 命令**；不要假设存在 `ruff`、`pytest`、`mypy` 或 `make` 工作流。

## 高层架构

### 1. 模板生成链路

- `cookiecutter.json` 只保留少量项目元数据输入：项目名、描述、作者、邮箱、时区、语言。
- `hooks/pre_gen_project.py` 仅负责渲染前校验；仓库没有 `post_gen_project.py`，模板渲染本身也不再自动创建虚拟环境、安装依赖或初始化 Git。
- 真正生成出来的项目骨架位于 `{{ cookiecutter.project }}`，并已包含 starter app、Celery 配置、Docker 编排、Nginx 配置和基础前端模板。

### 2. 生成项目的运行方式

- 开发环境通过 `docker/docker-compose.dev.yaml` 启动 `web`、`db`、`redis`、`celery-worker`、`celery-beat`。
- 生产环境通过 `docker/docker-compose.prd.yaml` 在开发栈基础上增加 `nginx`，由 Nginx 负责静态文件和反向代理。
- `entrypoint.sh` 按命令模式启动 `web-dev`、`web-prod`、`celery-worker`、`celery-beat`，避免为每个服务维护不同镜像逻辑。

### 3. 前端与应用骨架

- `core` 是默认 starter app，并提供首页、HTMX partial 示例、Alpine.js 交互示例。
- Tailwind 在开发阶段通过 CDN 提供，避免引入额外前端构建复杂度。
- `{{ cookiecutter.project }}/{{ cookiecutter.project }}/settings.py` 已固定接入 PostgreSQL、Redis、Celery、Sentry 与 `django-htmx`。

## 关键约定

- 这是模板仓库，修改 `{{ cookiecutter.project }}` 下的文件时要保留 `{{ ... }}` 占位语法，不能替换成具体项目名或固定值。
- 该仓库现在是 **固定栈模板**；不要重新引入 `project_type`、`use_async`、`use_sentry` 之类的组合开关。
- 生成项目使用单一 `.env.example` 作为环境变量事实源；变更配置时，应同步检查 `.env.example`、`settings.py`、`docker-compose` 与 README。
- Docker-only 开发是默认路径；除非用户明确要求，不要回退到“宿主机跑 Django、容器只跑依赖”的模式。
- 生成项目命令统一走 `./cmd.sh {bootstrap|dev|prod|manage|test}`；不要编造宿主机 `python manage.py`、`pip install -r requirements.txt` 或其他非容器化主流程。
- 模板调试应优先使用 `tools/validate_template.py` 进行渲染与 compose 校验，而不是手工推断生成结果。
