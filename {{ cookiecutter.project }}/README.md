# {{ cookiecutter.project }}
**项目简介**：{{ cookiecutter.description }}

## 快速开始
1. 创建开发环境

    ```sh
    # 创建环境变量配置文件
    cp .env.example .env

    # 创建开发环境
    docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d
    ```

2. 创建APP

    ```sh
    # 在项目根目录下运行如下命令创建应用(请修改`myapp`为实际名称)
    uv run manage.py startapp myapp
    ```

3. 创建功能  
    接下来在APP中创建一个简单的功能。
    
    创建视图：打开`myapp/views.py`，添加一下内容：

    ```py  
    import logging

    from django.http import JsonResponse

    logger = logging.getLogger(__name__)


    def index(request):
        logger.info("Index page accessed")
        return JsonResponse({"message": "Hello, world!"})
    ```

    配置URL：创建`myapp/urls.py`文件，输入以下内容：

    ```py
    from django.urls import path

    from . import views

    urlpatterns = [
        path("", views.index, name="index"),
    ]
    ```

4. 启用APP  
    打开`{{ cookiecutter.project }}/settings.py`,添加`myapp`到安装的app列表中。
    
    ```py
    INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       # 在末尾添加自建的APP
       'myapp'
    ]
    ```
    
    打开`{{ cookiecutter.project }}/urls.py`,添加`myapp`的URL配置。
    
    ```py
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        # 添加myapp的url配置
        path('', include('myapp.urls')),
    ]
    ```

5. 运行服务  
    在终端运行如下命令：

    ```py
    # 初始化数据库
    uv run manage.py migrate

    # 启动开发服务器
    uv run manage.py runserver
    ```

6. 访问功能
  打开浏览器，输入`http://localhost:8000`,如果显示`{"message": "Hello, world!"}`则表示访问正常。

## 项目结构
```
├── docker                                   (docker相关文件)
│   ├── nginx                                (一级Nginx示例)
│   │   ├── nginx.conf
│   │   ├── docker-compose.yaml
│   │   └── sites                            (站点配置目录)
│   ├── .env.example                         (生产环境变量配置)
│   ├── docker-compose.dev.yaml              (用于配置开发环境)
│   ├── docker-compose.prd.yaml              (用于生产环境部署)
│   └── nginx.conf                           (二级Nginx配置)
├── Dockerfile                               (用于构建项目镜像)
├── entrypoint.sh                            (容器入口脚本)  
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
├── {{ cookiecutter.project }}               (Django项目)
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

# 创建数据库迁移
uv run manage.py makemigrations

# 执行数据库迁移
uv run manage.py migrate

# 启动开发服务器
uv run manage.py runserver

# 创建后台管理员（交互式，按需）
uv run manage.py createsuperuser

# 销毁外部环境并清除数据
docker compose -f docker/docker-compose.dev.yaml down -v
```
**注意**：创建APP后需要启用APP，操作步骤见 [快速开始](#快速开始)

### 创建API视图
使用ninja可以再Django中创建类似FastApi的API。具体如下：

在`myapp/views.py`文件中创建视图函数：

```py
import logging

from ninja import Router, Schema


router = Router()
logger = logging.getLogger(__name__)

class AnalysisRequest(Schema):
    text:str

class AnalysisResponse(Schema):
    sentiment: str

@router.post("/analysis", response=AnalysisResponse)
def analysis(request, data: AnalysisRequest) -> AnalysisResponse:
    text = data.text
    return AnalysisResponse(sentiment='positive')
```

在`myapp/urls.py`文件中添加URL规则：

```py
from django.urls import path
from ninja import NinjaAPI

from .views import router

api = NinjaAPI()
api.add_router("/api", router)

urlpatterns = [
    path("", api.urls),
]
```

在`{{ cookiecutter.project }}/urls`中添加APP的URL配置：

```py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
]
```

启动web服务，查看结果：
```py
# 新建终端窗口，启动开发服务器
uv run manage.py runserver
```

从`localhost:8000/api/analysis`访问API。

**注意**：快速测试可以通过`localhost:8000/docs`页面可视化快速测试接口。


### 创建Celery任务
在`{{ cookiecutter.project }}`中创建`celery.py`文件，并添加以下内容：

```py
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.project }}.settings')

app = Celery('{{ cookiecutter.project }}')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

```

在APP中创建`tasks.py`文件

```sh
touch myapp/tasks.py
```

在`tasks.py`中创建任务，例如：

```py
import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    # 模拟一个耗时操作
    time.sleep(5)
    return x + y
```

在`views.py`文件中创建对应的视图函数：

```py
from celery.result import AsyncResult
from django.http import JsonResponse

from .tasks import add

def async_add_view(request):
    '''
    创建一个简易的异步任务
    '''
    result = add.delay(1, 2)
    return JsonResponse({"task_id": result.id})


def get_task_status(request):
    '''
    查看异步任务状态，获取异步任务结果
    '''
    task_id = request.GET.get("task_id")
    if not task_id:
        return JsonResponse({"error": "Missing task_id"}, status=400)

    task_result = AsyncResult(task_id)

    result = {"task_id": task_id, "status": task_result.status, "result": task_result.result if task_result.ready() else None}
    return JsonResponse(result)
```

在`urls.py`中配置URL规则：

```py
from django.urls import path

from . import views

urlpatterns = [
    path('async-add/', views.async_add_view, name='async_add'),
    path('task-status/', views.get_task_status, name='get_task_status'),
]
```

启动服务，包括web服务和Celery服务：

```py
# 新建终端窗口，启动开发服务器
uv run manage.py runserver

# 新建终端窗口，启动Celery，默认启动一个worker，通过-c指定并发数
uv run celery -A {{ cookiecutter.project }} worker -l info -c 4
```

至此，可以通过`async-add/`发起一个异步任务，再通过`task-status/`获取任务执行结果和状态。

```text
# 浏览器访问发起异步任务
http://localhost:8000/async-add/

# 返回任务ID（每次访问ID会不同）
{"task_id": "9e0b6465-cff9-40f6-9cf8-1e9ccac159a2"}

# 浏览器访问获取任务状态
http://localhost:8000/task-status/?task_id=9e0b6465-cff9-40f6-9cf8-1e9ccac159a2

# 返回任务状态
{"task_id": "9e0b6465-cff9-40f6-9cf8-1e9ccac159a2", "status": "SUCCESS", "result": 3}
```

**注意**：如果要创建定时任务，需要在`settings.py`中添加如下配置：

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 在末尾添加
    'django_celery_beat',
]
```

### 示例

以下展示的是`myapp/views.py`的完整代码示例：

```py
# myapp/views.py
import logging

from celery.result import AsyncResult
from django.http import JsonResponse
from ninja import Router, Schema

from .tasks import add

logger = logging.getLogger(__name__)

# 简单视图
def index(request):
    logger.info("Index page accessed")
    return JsonResponse({"message": "Hello, world!"})


# API视图
router = Router()
logger = logging.getLogger(__name__)


class AnalysisRequest(Schema):
    text: str


class AnalysisResponse(Schema):
    sentiment: str


@router.post("/analysis", response=AnalysisResponse)
def analysis(request, data: AnalysisRequest) -> AnalysisResponse:
    text = data.text
    return AnalysisResponse(sentiment='positive')


# Celery异步任务视图
def async_add_view(request):
    '''
    创建一个简易的异步任务
    '''
    result = add.delay(1, 2)
    return JsonResponse({"task_id": result.id})


# Celery任务状态视图
def get_task_status(request):
    '''
    查看异步任务状态，获取异步任务结果
    '''
    task_id = request.GET.get("task_id")
    if not task_id:
        return JsonResponse({"error": "Missing task_id"}, status=400)

    task_result = AsyncResult(task_id)

    result = {"task_id": task_id, "status": task_result.status, "result": task_result.result if task_result.ready() else None}
    return JsonResponse(result)
```

以下展示的是`myapp/urls.py`的完整代码示例：

```py
# myapp/urls.py
from django.urls import path
from ninja import NinjaAPI

from . import views
from .views import router

api = NinjaAPI()
api.add_router("/api", router)

urlpatterns = [
    path("", views.index, name="index"),
    path("", api.urls),
    path('async-add/', views.async_add_view, name='async_add'),
    path('task-status/', views.get_task_status, name='get_task_status'),
]
```

以下展示的是`myapp/tasks.py`的完整代码示例：

```py
# myapp/tasks.py
import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    # 模拟一个耗时操作
    time.sleep(5)
    return x + y
```

以下展示的是`{{ cookiecutter.project }}/urls.py`的完整代码示例：

```py
# {{ cookiecutter.project }}/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

以下展示的是`{{ cookiecutter.project }}/celery.py`的完整代码示例：

```py
# {{ cookiecutter.project }}/celery.py
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.project }}.settings')

app = Celery('{{ cookiecutter.project }}')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
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
部署方案中，一级Nginx负责监听外部端口，并根据路径转发至不同的二级Nginx，二级nginx负责处理静态文件和动态请求。一级Nginx由项目外部维护，二级Nginx由各个项目独立维护。

**注意**：需要注意由于路径前缀和端口，需要特别注意重定向错误。

### 本地测试

本地测试阶段主要有两项工作：

#### 配置检查
需要检查nginx配置、compose配置和环境变量配置。

环境变量(`/docker/.env`)注意检查：
- FORCE_SCRIPT_NAME: 设置为项目路径前缀，例如`/blog`或`/analysis`
- ALLOWED_HOSTS: 设置为服务器HOST  
- DB_HOST: 数据库HOST，生产环境为`db`，本地测试可设置为`localhost`  
- REDIS_HOST: Redis HOST，生产环境为`redis`，本地测试可设置为`localhost`  
- DJANGO_SUPERUSER_USERNAME: 管理员用户名
- DJANGO_SUPERUSER_PASSWORD: 管理员密码
- SENTRY_DSN: sentry dsn地址

#### 服务启动

```sh
# 导出依赖
uv export --format requirements-txt > requirements.txt

# 构建镜像
docker compose -f docker/docker-compose.prd.yaml --env-file .env build web

# 创建nginx网络
docker network create nginx-network

# 启动镜像
docker compose -f docker/docker-compose.prd.yaml --env-file .env up -d

# 启动nginx一级代理
docker compose -f docker/nginx/docker-compose.yaml up -d
```

#### 服务关闭

```sh
# 关闭nginx一级代理
docker compose -f docker/nginx/docker-compose.yaml down -v

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
docker save {{ cookiecutter.project }}:0.1.0 -o deploy/{{ cookiecutter.project }}:0.1.0.tar

# 复制.env文件
cp docker/.env deploy/

# 复制一级nginx站点config文件
cp docker/nginx/sites/{{ cookiecutter.project }}.conf deploy/

# 复制二级nginx配置
cp docker/nginx.conf deploy/

# 复制compose文件
cp docker/docker-compose.prd.yaml deploy/

# 上传服务器
scp -r deploy user@server:/path/to/deploy -p port
```

#### 远端操作
```sh
cd /path/to/deploy

# 导入镜像
docker load -i {{ cookiecutter.project }}:0.1.0.tar

# 为镜像打标签
docker tag {{ cookiecutter.project }}:0.1.0 {{ cookiecutter.project }}:latest

# 创建nginx网络（如有则不用重复创建）
docker network create nginx-network

# 启动镜像
docker compose -f docker-compose.prd.yaml up -d

# 配置一级nginx
cp {{ cookiecutter.project }}.conf /path/to/nginx/sites

# 验证nginx配置
docker exec nginx nginx -t

# 重载nginx配置
docker exec -it nginx nginx -s reload
```

注意：项目部署假设已经启动了一级Nginx服务，如果没有启动一级Nginx服务，请先[启动一级Nginx服务](#启动一级nginx服务)。

## 启动一级nginx服务

### 服务结构
`/docker/nginx`文件夹中给出了一级Nginx服务的示例配置:

```
├── docker-compose.yaml         (nginx compose文件)
├── nginx.conf                  (nginx主配置)
└── sites                       (站点配置)
```

- nginx.conf  
    这是nginx服务的主配置文件，设置了一般性配置。  
    各个站点配置存放在`sites`中，在主配置中导入。

    注意：`worker_processes`和`worker_connections`可以根据实际需要调整。

- docker-compose.yaml  
    需关注端口配置。
    例如，如可用端口是`32156`,则需要将端口设置为`32156:80`。

### 服务启动

```sh
# 创建nginx网络（如有则不用重复创建）
docker network create nginx-network

# 启动nginx
docker compose -f docker/nginx/docker-compose.yaml up -d
```

**注意**：要特别注意一级nginx和web服务的启动顺序！此外，首个项目和后续项目略有不同。  

**首个**项目启动顺序：  
1. 启动站点web服务
2. 添加站点配置
3. **启动**一级Nginx

**后续**项目启动顺序：
1. 启动站点web服务
2. 添加站点配置
3. **重载**一级Nginx


## 快捷工具
项目根目录下的`cmd.sh`提供了常用的命令，便于快速启动项目开发：

### 开发环境
```sh
# 创建开发环境
./cmd.sh dev up 

# 销毁开发环境
./cmd.sh dev down
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