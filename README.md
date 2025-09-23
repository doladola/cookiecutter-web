# 项目简介
这是Django web项目模板。

## 使用方法
```sh
# 基于uv
uvx cookiecutter cookiecutter-web/
```

## 部署方法

### Nginx配置
Django项目在生产环境中需要使用Nginx做反向代理和静态文件服务，一台服务器上可以共用一个Nginx。使用环节主要包括三个步骤：
1. 创建Nginx网络
    `docker network create nginx_net`（首次创建时执行，仅执行一次即可）
1. 启动Nginx服务
    启动Nginx服务，为后续接入Web服务做准备。（首次启动时执行，仅执行一次即可）
2. 启动Web服务
    启动Django Web服务。Web服务在启动时要加入Nginx网络并导出静态文件。
3. 更新Nginx配置
    更新Nginx配置文件，添加Web服务的反向代理配置，并重新加载Nginx配置。
4. 重载Nginx配置
    加载Nginx的配置文件，让新配置生效。

#### Nginx目录结构
在`deploy/nginx`目录中有Nginx的配置示例。主要包括三个部分：
1. `nginx.conf`文件：Nginx的主配置文件
2. `vhosts/`目录：保存了各个Web服务站点的Nginx配置
3. `docker-compose.yml`文件：用于启动Nginx容器

#### 启动Nginx服务
执行以下命令启动Nginx服务：
```sh
cd deploy/nginx 
docker compose up -d
```
！注意：启动前要编辑`docker-compose，修正Nginx的端口！

### 启动web服务
执行以下命令启动Web服务：
```sh
cd deploy/django
docker compose up -d
```
！注意：启动前要编辑`docker-compose.yml`，修正Web服务的端口和环境变量文件路径！

### 更新Nginx配置
在`deploy/nginx/vhosts/`目录中添加Web服务的Nginx配置文件，配置示例见`nginx/vhosts/example.conf`。
注意要修改如下配置：
- web容器名
- server_name
- client_max_body_size

### 重载Nginx配置
执行以下命令重载Nginx配置：
```sh
docker exec -it nginx nginx -s reload
```





