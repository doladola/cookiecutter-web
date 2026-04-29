# {{ cookiecutter.project }}

**项目简介**：{{ cookiecutter.description }}

## 快速开始

```sh
cp .env.example .env
docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d
uv run manage.py migrate
uv run manage.py runserver
```

如果需要创建新应用：

```sh
uv run manage.py startapp myapp
```

## 常用命令

| 场景 | 命令 |
| --- | --- |
| 启动开发依赖 | `./cmd.sh dev up` |
| 停止开发依赖 | `./cmd.sh dev down` |
| 构建生产镜像（基于 `uv.lock`） | `./cmd.sh build` |
| 启动生产编排 | `./cmd.sh run` |
| 停止生产编排 | `./cmd.sh stop` |
| 数据库迁移 | `uv run manage.py migrate` |
| 启动 Django | `uv run manage.py runserver` |
| 启动 Celery Worker | `uv run celery -A {{ cookiecutter.project }} worker -l info` |

## 环境变量

- 复制根目录 `.env.example` 为 `.env`
- 本地开发默认使用 `localhost` 连接 PostgreSQL 和 Redis
- 生产 Compose 会覆盖 `DEBUG`、`DB_HOST`、`REDIS_HOST` 和 `FORCE_SCRIPT_NAME` 等容器内差异配置
- Celery 默认根据 `REDIS_HOST` / `REDIS_PORT` 自动推导 broker 与 result backend；只有自定义地址时才需要额外设置

## 文档

- [部署说明](docs/deployment.md)
- [项目结构](docs/project-structure.md)
- [开发示例](docs/examples.md)

## 可选能力

- `use_ninja`：生成后追加 Django Ninja 依赖，便于创建 API
- `use_sentry`：生成后追加 Sentry SDK，并在 `settings.py` 中读取对应配置
