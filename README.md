# cookiecutter-web

一个 **固定技术栈、Linux-only、对 Copilot CLI 友好的 Django 项目模板**。

生成结果默认包含：

- Django
- PostgreSQL
- Redis
- Celery + django-celery-beat
- HTMX + Alpine.js
- Tailwind CSS（开发期走 CDN）
- Docker
- Nginx（生产环境静态文件服务）
- Sentry

## 设计原则

- **固定栈**：不再通过模板开关组合不同技术栈
- **少变量**：Cookiecutter 只负责项目元数据，不承担复杂分支逻辑
- **Docker-only 开发**：生成项目默认在容器内运行 web / worker / beat / db / redis
- **低副作用渲染**：模板渲染不再自动创建虚拟环境、安装依赖或初始化 Git
- **无 post-gen 副作用**：仓库只保留 `hooks/pre_gen_project.py` 做输入校验，不再依赖 `post_gen_project.py`
- **可验证**：模板仓库提供渲染校验脚本，方便人工和 Copilot CLI 调试

## 渲染模板

```sh
uvx cookiecutter -f cookiecutter-web/
```

## 校验模板

```sh
python tools/validate_template.py
```

该脚本会：

1. 渲染一个临时项目
2. 检查关键文件是否存在
3. 运行开发 / 生产 compose 配置校验

## 模板输入

当前模板只保留少量项目元数据：

- `project`
- `description`
- `author`
- `email`
- `timezone`
- `language`

## 生成项目工作流

生成后的项目统一通过 `cmd.sh` 操作；不要再文档化宿主机 `python`、`pip`、虚拟环境或可选技术栈分支。

```sh
./cmd.sh bootstrap
./cmd.sh dev up
./cmd.sh manage migrate
./cmd.sh test
./cmd.sh prod up
```

## 仓库结构

- `cookiecutter.json`：模板输入定义
- `hooks/`：渲染前校验
- `{{ cookiecutter.project }}/`：生成项目骨架
- `tools/validate_template.py`：模板渲染校验脚本
- `.github/copilot-instructions.md`：面向 Copilot 会话的仓库说明

