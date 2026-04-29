# 项目结构

```text
.
├── docker/                         # Compose 与 Nginx 配置
│   ├── docker-compose.dev.yaml     # 本地开发依赖（PostgreSQL / Redis）
│   ├── docker-compose.prd.yaml     # 生产编排参考
│   ├── nginx.conf                  # 项目级 Nginx 配置
│   └── nginx/                      # 一层 Nginx 示例
├── docs/                           # 详细文档
├── {{ cookiecutter.project }}/     # Django project package
├── Dockerfile                      # 基于 uv.lock 构建镜像
├── entrypoint.sh                   # 容器启动、迁移、collectstatic、初始化管理员
├── manage.py
├── pyproject.toml
├── README.md
├── .env.example                    # 唯一的环境变量模板
└── uv.lock
```

## 关键文件

- `pyproject.toml` + `uv.lock`：应用依赖定义与锁定结果
- `.env.example`：开发与部署共享的环境变量模板
- `cmd.sh`：常用开发/部署辅助命令
- `docker/docker-compose.dev.yaml`：本地开发依赖
- `docker/docker-compose.prd.yaml`：生产编排参考
- `{{ cookiecutter.project }}/settings.py`：Django 配置，读取根目录 `.env`
