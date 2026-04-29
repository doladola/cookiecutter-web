# 开发示例

## 创建一个简单页面

1. 创建应用：

   ```sh
   uv run manage.py startapp myapp
   ```

2. 在 `myapp/views.py` 中添加视图：

   ```py
   import logging

   from django.http import JsonResponse

   logger = logging.getLogger(__name__)


   def index(request):
       logger.info("Index page accessed")
       return JsonResponse({"message": "Hello, world!"})
   ```

3. 在 `myapp/urls.py` 中注册路由：

   ```py
   from django.urls import path

   from . import views

   urlpatterns = [
       path("", views.index, name="index"),
   ]
   ```

4. 在 `{{ cookiecutter.project }}/urls.py` 中挂载应用：

   ```py
   from django.contrib import admin
   from django.urls import include, path

   urlpatterns = [
       path("admin/", admin.site.urls),
       path("", include("myapp.urls")),
   ]
   ```

## Django Ninja 示例

如果生成项目时启用了 `use_ninja`，可以在应用中添加 API：

```py
from ninja import Router, Schema

router = Router()


class AnalysisRequest(Schema):
    text: str


class AnalysisResponse(Schema):
    sentiment: str


@router.post("/analysis", response=AnalysisResponse)
def analysis(request, data: AnalysisRequest) -> AnalysisResponse:
    return AnalysisResponse(sentiment="positive")
```

然后在应用 `urls.py` 中挂载 `NinjaAPI` 并运行 `uv run manage.py runserver`，通过 `/docs` 查看交互式文档。

## Celery 示例

模板默认已经包含 Redis、Celery 和 `django-celery-beat`，可直接在应用中添加任务：

```py
from celery import shared_task


@shared_task
def add(x, y):
    return x + y
```

启动 worker：

```sh
uv run celery -A {{ cookiecutter.project }} worker -l info
```
