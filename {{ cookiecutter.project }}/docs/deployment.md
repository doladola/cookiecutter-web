# 部署说明

## 配置入口

1. 复制根目录 `.env.example` 为 `.env`
2. 按需修改以下变量：
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`
   - `FORCE_SCRIPT_NAME`
   - `DJANGO_SUPERUSER_*`
   - `SENTRY_*`

`docker/docker-compose.prd.yaml` 会在容器内覆盖这些运行时差异：

- `DEBUG=False`
- `DB_HOST=db`
- `REDIS_HOST=redis`
- `FORCE_SCRIPT_NAME=/{{ cookiecutter.project }}`

因此单一 `.env` 可以同时服务开发和部署，不需要再维护第二份 `docker/.env`。

## 构建镜像

项目镜像基于 `uv.lock` 构建，不再导出 `requirements.txt`：

```sh
./cmd.sh build
```

等价的底层命令：

```sh
docker compose -f docker/docker-compose.prd.yaml --env-file .env build web
```

## 启动服务

```sh
./cmd.sh run
```

这会：

1. 确保 `nginx-network` 存在
2. 启动项目自己的生产编排
3. 启动 `docker/nginx/docker-compose.yaml` 中的一层 Nginx 示例

## 停止服务

```sh
./cmd.sh stop
```

## 手动部署参考

### 本地打包

```sh
mkdir deploy
mkdir -p deploy/docker
mkdir -p deploy/docker/nginx/sites
docker save {{ cookiecutter.project }}:0.1.0 -o deploy/{{ cookiecutter.project }}:0.1.0.tar
cp .env deploy/
cp docker/nginx/sites/{{ cookiecutter.project }}.conf deploy/docker/nginx/sites/
cp docker/nginx.conf deploy/docker/
cp docker/docker-compose.prd.yaml deploy/docker/
```

### 服务器侧

```sh
cd /path/to/deploy
docker load -i {{ cookiecutter.project }}:0.1.0.tar
docker tag {{ cookiecutter.project }}:0.1.0 {{ cookiecutter.project }}:latest
docker network create nginx-network
docker compose -f docker/docker-compose.prd.yaml --env-file .env up -d
```

## Nginx 路径前缀说明

该模板假设项目挂载在路径前缀 `/{{ cookiecutter.project }}` 下：

- 外层 Nginx 根据路径前缀转发到项目自己的 Nginx
- 项目 Nginx 再把静态文件直接返回，把动态请求转给 Django
- Django 侧通过 `FORCE_SCRIPT_NAME` 生成带前缀的静态资源与路由 URL

如果你的部署不是路径前缀模式，请同步调整：

- `docker/nginx/sites/{{ cookiecutter.project }}.conf`
- `docker/docker-compose.prd.yaml`
- `.env` 中的 `FORCE_SCRIPT_NAME`
