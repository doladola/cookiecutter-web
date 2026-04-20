# {{ cookiecutter.project }}

{{ cookiecutter.description }}

这是一个固定技术栈的 Django 项目，默认包含：

- Django
- PostgreSQL
- Redis
- Celery + django-celery-beat
- HTMX + Alpine.js
- Tailwind CSS（开发期 CDN）
- Docker
- Nginx（生产环境）
- Sentry

## 快速开始

```sh
./cmd.sh bootstrap
./cmd.sh dev up
```

`cmd.sh` 会负责 Docker-only 的开发/生产/管理/测试流程；不要切换回宿主机虚拟环境工作流。

打开 <http://localhost:8000>。

## 常用命令

```sh
# 启动开发环境
./cmd.sh dev up

# 停止开发环境
./cmd.sh dev down

# 查看日志
./cmd.sh dev logs
./cmd.sh prod logs

# 进入 web 容器
./cmd.sh dev shell

# 执行 Django 管理命令
./cmd.sh manage createsuperuser
./cmd.sh manage makemigrations
./cmd.sh manage migrate

# 运行测试
./cmd.sh test

# 启动生产编排
./cmd.sh prod up

# 停止生产编排
./cmd.sh prod down
```

## 项目结构

```text
.
├── core/                         starter app
├── docker/                       Docker Compose 与 Nginx 配置
├── {{ cookiecutter.project }}/   Django project package
├── .env.example                  统一环境变量示例
├── cmd.sh                        Linux-only helper commands
├── Dockerfile                    统一镜像构建入口
├── entrypoint.sh                 容器入口脚本
├── manage.py
└── requirements.txt
```

## 开发约定

- 开发模式为 **Docker-only**
- 项目命令统一走 `./cmd.sh {bootstrap|dev|prod|manage|test}`
- `core` 是默认 starter app
- HTMX、Alpine.js、Tailwind 已在基础模板中接入
- Tailwind 在开发阶段通过 CDN 提供；生产阶段可再增加单独构建脚本
- Sentry 默认启用集成代码，但只有设置 `SENTRY_DSN` 后才会上报
