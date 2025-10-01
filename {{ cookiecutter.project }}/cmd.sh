#!/bin/bash

# 退出脚本，如果任何命令失败
set -e

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示用法
usage() {
    echo -e "${YELLOW}用法: $0 {dev|build|run|stop}${NC}"
    echo "  dev   [up|down]   - 启动或停止开发环境依赖 (默认: up)"
    echo "  build             - 构建项目镜像"
    echo "  run               - 启动项目服务 (一级Nginx和项目镜像)"
    echo "  stop              - 停止项目服务"
    exit 1
}

# 功能1: 启停开发环境
dev_env() {
    case "$1" in
        up|"" )
            echo -e "${GREEN}启动开发环境依赖...${NC}"
            docker compose -f docker/docker-compose.dev.yaml --env-file .env up -d
            echo -e "${GREEN}开发环境已启动。${NC}"
            ;;
        down )
            echo -e "${GREEN}停止并移除开发环境依赖...${NC}"
            docker compose -f docker/docker-compose.dev.yaml down -v
            echo -e "${GREEN}开发环境已停止。${NC}"
            ;;
        * )
            usage
            ;;
    esac
}

# 功能2: 构建项目镜像
build_image() {
    echo -e "${GREEN}导出依赖到 requirements.txt...${NC}"
    uv export --format requirements-txt > requirements.txt
    echo -e "${GREEN}开始构建项目镜像...${NC}"
    docker compose -f docker/docker-compose.prd.yaml --env-file docker/.env build web
    echo -e "${GREEN}镜像构建完成。${NC}"
    echo -e "${GREEN}清理悬空镜像...${NC}"
    docker image prune
    echo -e "${GREEN}清理完成。${NC}"
}

# 功能3: 启动项目服务
run_services() {
    if ! docker network inspect nginx-network >/dev/null 2>&1; then
        echo -e "${GREEN}Nginx网络不存在，正在创建...${NC}"
        docker network create nginx-network
    else
        echo -e "${GREEN}Nginx网络已存在，跳过创建。${NC}"
    fi
    echo -e "${GREEN}启动项目服务...${NC}"
    docker compose -f docker/docker-compose.prd.yaml --env-file docker/.env up -d
    echo -e "${GREEN}启动一级Nginx服务...${NC}"
    docker compose -f docker/nginx/docker-compose.yaml up -d
    echo -e "${GREEN}所有服务已启动。${NC}"
}

# 功能3: 停止项目服务
stop_services() {
    echo -e "${GREEN}停止一级Nginx服务...${NC}"
    docker compose -f docker/nginx/docker-compose.yaml down
    echo -e "${GREEN}停止项目服务...${NC}"
    docker compose -f docker/docker-compose.prd.yaml --env-file docker/.env down -v
    echo -e "${GREEN}所有服务已停止。${NC}"
    docker network rm nginx-network || true
    echo -e "${GREEN}Nginx网络已移除。${NC}"
}

# 主逻辑
case "$1" in
    dev )
        dev_env "$2"
        ;;
    build )
        build_image
        ;;
    run )
        run_services
        ;;
    stop )
        stop_services
        ;;
    * )
        usage
        ;;
esac

exit 0