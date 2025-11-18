# 项目简介
Django项目脚手架，用于快速创建Django web项目。

## 使用方法
```sh
# 基于uv
uvx cookiecutter -f cookiecutter-web/
```

## 核心信息
1. Django版本

    项目基于Django(5.2.2)版本，未测试其他版本兼容性。

2. 版本管理

    项目基于`uv`构建版本管理。

3. 部署方式

    项目基于docker部署，自动启动web服务依赖的数据库、缓存、任务队列等依赖。
    部署结构上采取两级nginx级联。
    一级nginx用于不同web服务请求的动态转发。
    二级nginx用于向本项目的web服务转发动态请求，并提供本项目的静态文件服务。

    > WHY？
    > - 独立性：两级级联的方式能最大限度隔离不同项目。
    > - 统一性：两级级联的方式能统一管理服务器上的请求。


## 功能简介
- 自动配置：脚手架自动配置数据库、缓存、任务队列、日志监控等
- 环境配置：脚手架提供了本地开发的环境配置，支持一件创建本地研发环境
- 部署配置：脚手架提供了服务部署的配置、脚本和说明，减少项目部署的难度
- VsCode集成：自动配置VsCode开发环境，支持跨平台开发（Windows/Linux）


## VsCode集成

生成的项目自动包含VsCode配置，提供开箱即用的开发体验：

### 配置内容
项目在`.vscode/settings.json`中预配置了以下内容：

1. **Python解释器路径**
   - 根据选择的平台（Windows/Linux）自动配置Python解释器路径
   - Windows: `${workspaceFolder}\.venv\Scripts\python.exe`
   - Linux: `${workspaceFolder}/.venv/bin/python`

2. **测试框架配置**
   - 启用Django unittest测试框架
   - 自动发现`test*.py`文件中的测试

### 使用建议
1. 使用VsCode打开生成的项目目录
2. VsCode会自动识别Python虚拟环境
3. 可以直接使用VsCode的测试浏览器运行Django测试
4. 支持调试Django应用和测试用例

### 扩展推荐
为获得最佳开发体验，推荐安装以下VsCode扩展：
- Python (Microsoft)
- Django (Baptiste Darthenay)
- Pylance (Microsoft)

## 后续计划
- 支持异步框架
- 支持无数据库模式
