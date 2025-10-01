# {{ cookiecutter.project }}
**项目简介**：This Is My Awesom Project!

## 项目结构
```
├── docker                                   (docker相关文件)
│   ├── nginx                                (一级Nginx示例)
│   │   ├── nginx.conf
│   │   ├── docker-compose.yaml
│   │   └── sites                            (站点配置目录)
│   ├── .env                                 (生产环境变量配置)
│   ├── docker-compose.dev.yaml              (用于配置开发环境)
│   ├── docker-compose.prd.yaml              (用于生产环境部署)
│   └── nginx.conf                           (二级Nginx配置)
├── Dockerfile                               (用于构建项目镜像)
├── entrypoint.sh                            (容器入口脚本) 
├── log                                      (日志文件夹)    
│   └── {{ cookiecutter.project }}.log
├── manage.py                                (Django项目管理脚本)
├── media                                    (用户上传文件存放目录)
├── myapp                                    (Django应用)
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── models.py
│   ├── tasks.py                             (Celery任务)
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── {{ cookiecutter.project }}                                   (Django项目)
│   ├── asgi.py
│   ├── celery.py                            (Celery配置)
│   ├── __init__.py
│   ├── settings.py                          (Django配置)
│   ├── urls.py
│   └── wsgi.py
├── pyproject.toml
├── README.md
├── static                                   (静态文件目录)
├── .dockerignore                            (Docker忽略文件)
├── .env                                     (环境变量配置文件)
├── .env.example                             (环境变量配置文件示例)
├── .gitignore                               (Git忽略文件)
├── .python-version                          
├── .vscode                                  (vs code配置)
└── uv.lock
```

## 配置说明
```
# 设定manage.py文件路径
MANAGE_PY_PATH=manage.py

# 设定Docker image version
VERSION=0.1.0

# 设置secret key
# generate your own using `python -c "import secrets; print(secrets.token_urlsafe())"`
SECRET_KEY=replace-with-your-key

# 是否启动Debug模式
# 开发是设置为True，发布生产调整为False
DEBUG=True

# 设置allowed hosts, comma separated, e.g. localhost,example.com
# 发布生产时要添加服务器的HOST
ALLOWED_HOSTS=localhost,127.0.0.1

# 日志路径
LOGFILE=log/{{ cookiecutter.project }}.log

# 设置后台管理员信息
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL={{ cookiecutter.project }}@{{ cookiecutter.project }}.com
DJANGO_SUPERUSER_PASSWORD=admin123

# 服务进程数
GUNICORN_WORKERS=4
# 服务线程数
GUNICORN_THREADS=4

# 数据库配置
DB_NAME={{ cookiecutter.project }}
DB_USER={{ cookiecutter.project }}
DB_PASSWORD={{ cookiecutter.project }}
DB_HOST=localhost
# 端口固定，修改无效
DB_PORT=5432
DB_CONN_MAX_AGE=60

# redis配置
REDIS_HOST=localhost
# 端口固定，修改无效
REDIS_PORT=6379

# celery配置
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# sentry配置
SENTRY_DSN=your-dns-url
SENTRY_LOG=True
SENTRY_TRACES_SAMPLE_RATE=0.01
SENTRY_PROFILE=trace
```

## 项目开发
开始项目开发前，先创建外部环境依赖，具体如下：
```sh
# 创建开发环境
docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d

# 创建应用
uv run manage.py startapp myapp

# 初始化数据库
uv run manage.py migrate

# 启动开发服务器
uv run manage.py runserver

# 启动Celery，默认启动一个worker，通过-c指定并发数
uv run celery -A {{ cookiecutter.project }} worker -l info -c 4

# 创建后台管理员（交互式，按需）
uv run manage.py createsuperuser

# 销毁外部环境并清除数据
docker compose -f docker/docker-compose.dev.yaml down -v
```

## 操作手册

常用操作：
```sh
# 创建项目
uvx cookiecutter -f cookiecutter-web
```

## 项目部署

### 部署结构
部署方案以Nginx反向代理为基础，假设有两个Django项目：blog和analysis，部署结构如下：
```
客户端 → http://host:port/
       ↓
一级Nginx（监听port端口）
       ├─ 路径以/blog/开头 → 转发至blog项目二级Nginx（80端口）
       │                     ↓
       │              blog二级Nginx
       │                     ├─ 静态请求 → 直接返回/static/目录文件
       │                     └─ 动态请求 → 转发至blog的Django服务（8000端口）
       │
       └─ 路径以/analysis/开头 → 转发至analysis项目二级Nginx（80端口）
                             ↓
                      analysis二级Nginx
                             ├─ 静态请求 → 直接返回/static/目录文件
                             └─ 动态请求 → 转发至analysis的Django服务（8000端口）
```
部署方案中，一级Nginx负责监听外部端口，并根据路径转发至不同的二级Nginx，二级nginx负责处理静态文件和动态请求。
该方案需要注意由于路径前缀问题，需要特别注意重定向错误。

### 本地测试

本地测试阶段主要有两项工作：

#### 配置检查
需要检查nginx配置、compose配置和环境变量配置。

环境变量(`/docker/.env`)注意检查：
- SITE
- ALLOWED_HOSTS  
- DB_HOST  
- REDIS_HOST  

#### 服务启动

```sh
# 导出依赖
uv export --format requirements-txt > requirements.txt

# 构建镜像
docker compose -f docker/docker-compose.prd.yaml --env-file .env build {{ cookiecutter.project }}

# 创建nginx网络
docker network create nginx-network

# 启动镜像
docker compose -f docker/docker-compose.prd.yaml --env-file .env up -d

# 启动nginx一级代理
docker compose -f docker/nginx/docker-compose.yaml
```

#### 服务关闭

```sh
# 关闭nginx一级代理
docker compose -f docker/nginx/docker-compose.yaml

# 关闭项目服务
docker compose -f docker/docker-compose.prd.yaml --env-file .env down -v

# 删除nginx网络
docker network rm nginx-network
```

### 生产发布

#### 本地操作
```sh
# 创建deploy目录
mkdir deploy

# 导出镜像
docker save {{ cookiecutter.project }}:0.1.0 -o /deploy/{{ cookiecutter.project }}:0.1.0.tar

# 复制.env文件
cp docker/.env /deploy/

# 复制vhost config文件
cp docker/{{ cookiecutter.project }}.vhost.conf /deploy/

# 复制compose文件
cp docker/docker-compose.prd.yaml /deploy/

# 上传服务器
scp -r deploy user@server:/path/to/deploy -p port
```

#### 远端操作
```sh
cd /path/to/deploy

# 导入镜像
docker load -i {{ cookiecutter.project }}:0.1.0.tar

# 启动镜像
docker compose -f docker-compose.prd.yaml up -d

# 配置nginx
cp {{ cookiecutter.project }}.vhost.conf /path/to/nginx/vhost

# 验证nginx配置
docker exec nginx nginx -t

# 重载nginx配置
docker exec -it nginx nginx -s reload
```

注意：项目部署假设已经启动了Nginx服务，如果没有启动Nginx服务，请先启动Nginx服务。

## 启动Nginx服务
`nginx`文件夹中给出了Nginx服务的示例配置:

```
├── docker-compose.yaml         (nginx compose文件)
├── nginx.conf                  (nginx主配置)
└── vhosts                      (站点配置)
```

- nginx.conf  
    这是nginx服务的主配置文件，设置了一般性配置。  
    各个站点配置存放在`vhosts`中，在主配置中导入。

    注意：`worker_processes`和`worker_connections`可以根据实际需要调整。

- docker-compose.yaml  
    需关注端口配置。
    例如，如可用端口是`32156`,则需要将端口设置为`32156:80`。

### 启动nginx服务
```sh
# 创建nginx网络（如有则不用重复创建）
docker network create nginx-network

# 启动nginx
docker compose -f nginx/docker-compose.yaml up -d
```

## 常用工具

### 生成随机密码
```python
import secrets
import string

# 生成一个长度为12的随机密码
alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for _ in range(12))
print(password)
```

### 生成secret key
```python
import secrets
print(secrets.token_urlsafe())
```