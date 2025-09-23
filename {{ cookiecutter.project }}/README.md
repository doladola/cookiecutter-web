# {{ cookiecutter.project }}
**项目简介**：{{ cookiecutter.description }}

## 环境配置

## 项目结构


## 操作手册
### UV操作
UV[安装](https://docs.astral.sh/uv/getting-started/installation/)：
```sh
# mac or linux with curl
curl -LsSf https://astral.sh/uv/install.sh | sh
# mac or linux with wget
wget -qO- https://astral.sh/uv/install.sh | sh

# windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

常用操作：
```sh
# 创建项目
uvx cookiecutter -f cookiecutter-web

```

### Django操作
```sh
# 创建APP--假设名称为myapp
uv run manage.py startapp myapp
```

### sentry
```sh
# 安装sentry-sdk
uv add "sentry-sdk[django]"
```

配置settings.py
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://a10a24e15383750b578745600b2225fb@o4509948417343488.ingest.us.sentry.io/4509948419244032",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_logs=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profile_session_sample_rate to 1.0 to profile 100%
    # of profile sessions.
    profile_session_sample_rate=1.0,
    # Set profile_lifecycle to "trace" to automatically
    # run the profiler on when there is an active transaction
    profile_lifecycle="trace",
)
```

验证配置是否成功
```python
# 在views.py中添加如下代码from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    # ...
]
```


