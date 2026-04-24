# cookiecutter-web

一个面向 Django Web 项目的 Cookiecutter 脚手架，用来快速生成带有开发、部署和常用基础设施配置的项目骨架。

## 适用场景

- 想快速初始化一个基于 Django 的 Web 项目
- 希望默认带上 PostgreSQL、Redis、Celery、Gunicorn、Nginx 等常见生产组件
- 希望使用 `uv` 管理 Python 环境与依赖，并保留 Docker-first 的交付方式

## 当前版本基线

| 项目 | 版本 / 镜像 |
| --- | --- |
| Django | `6.0` 系列 |
| Python 基础镜像 | `astral/uv:python3.13-trixie-slim` |
| PostgreSQL | `postgres:17-alpine` |
| Redis | `redis:7-alpine` |
| Python 依赖管理 | `uv` |

## 模板会生成什么

生成后的项目默认包含：

- Django 项目基础结构（`settings.py`、`urls.py`、`asgi.py`、`wsgi.py`）
- `uv` 驱动的 Python 项目配置与依赖安装流程
- PostgreSQL、Redis、Celery、`django-celery-beat` 的基础接线
- 本地开发用的 Docker Compose 配置
- 面向部署的 Dockerfile、Compose、entrypoint 和 Nginx 配置示例
- 可选的 Django Ninja 与 Sentry 集成

## 仓库结构

```text
.
├── cookiecutter.json              # 模板变量与提示项
├── hooks/                         # 生成前/后的校验与初始化逻辑
└── {{ cookiecutter.project }}/    # 生成项目时使用的模板目录
```

> 注意：`{{ cookiecutter.project }}` 目录中的内容是模板源文件，不是当前仓库里可直接运行的 Django 项目。

## 快速开始

### 1. 生成项目

在仓库根目录执行：

```sh
uvx cookiecutter -f .
```

如果你是在其他目录引用此仓库，也可以把 `.` 替换成仓库路径或 Git 地址。

### 2. 进入生成后的项目目录

```sh
cd <your-project-name>
```

### 3. 初始化本地开发依赖

```sh
cp .env.example .env
docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d
```

这会启动本地开发需要的 PostgreSQL 和 Redis。

### 4. 启动 Django 开发流程

```sh
uv run manage.py migrate
uv run manage.py runserver
```

如果需要新增应用：

```sh
uv run manage.py startapp myapp
```

## 生成后的典型开发流

```sh
# 安装/同步依赖由模板在生成后自动完成

# 启动本地依赖
docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d

# 数据库迁移
uv run manage.py makemigrations
uv run manage.py migrate

# 启动 Django
uv run manage.py runserver

# 启动 Celery Worker
uv run celery -A <your-project-name> worker -l info
```

## 部署方式概览

生成后的项目采用 Docker-first 交付方式：

- 应用容器基于 `astral/uv:python3.13-trixie-slim`
- 项目内置开发与生产两套 Compose 配置
- 默认使用 PostgreSQL、Redis、Celery
- 提供项目级二级 Nginx 配置，方便接入统一入口网关

仓库中的模板还附带：

- `docker/docker-compose.dev.yaml`：本地研发依赖
- `docker/docker-compose.prd.yaml`：生产部署参考编排
- `docker/nginx/`：Nginx 配置示例
- `cmd.sh`：常用开发/部署辅助命令

## 可选能力

- `use_ninja`：生成后附加 Django Ninja 依赖
- `use_sentry`：生成后附加 Sentry SDK 并在设置中启用对应配置

## 关键实现说明

- 依赖不是直接写死在模板 `pyproject.toml` 中，而是在生成后由 `hooks/post_gen_project.py` 使用 `uv add --link-mode=copy` 注入
- Redis 和 Celery 属于模板默认能力，不作为用户可选项关闭
- 生成后的项目 README 会提供更细的项目内使用说明、环境变量说明和部署步骤

## 验证模板

本仓库最直接的 smoke test 是在仓库根目录执行：

```sh
uvx cookiecutter -f .
```

成功生成项目后，再进入生成目录执行 Django 与 Docker 相关命令，即可验证模板是否符合预期。
