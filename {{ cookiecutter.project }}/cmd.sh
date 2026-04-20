#!/bin/bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    echo -e "${YELLOW}用法:${NC} $0 {bootstrap|dev|prod|manage|test}"
    echo "  bootstrap              - 若 .env 不存在，则从 .env.example 创建"
    echo "  dev up|down|logs|shell - 开发环境"
    echo "  prod up|down|logs      - 生产编排"
    echo "  manage <args...>       - 在开发 web 容器中执行 manage.py"
    echo "  test                   - 在开发 web 容器中运行测试"
    exit 1
}

bootstrap() {
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${GREEN}.env 已创建。${NC}"
    fi
}

compose_dev() {
    docker compose -f docker/docker-compose.dev.yaml --env-file .env "$@"
}

compose_prod() {
    docker compose -f docker/docker-compose.prd.yaml --env-file .env "$@"
}

case "${1:-}" in
    bootstrap )
        bootstrap
        ;;
    dev )
        bootstrap
        case "${2:-up}" in
            up )
                compose_dev up --build -d
                ;;
            down )
                compose_dev down -v
                ;;
            logs )
                if [ -n "${3:-}" ]; then
                    compose_dev logs -f "$3"
                else
                    compose_dev logs -f
                fi
                ;;
            shell )
                compose_dev exec web sh
                ;;
            * )
                usage
                ;;
        esac
        ;;
    prod )
        bootstrap
        case "${2:-up}" in
            up )
                compose_prod up --build -d
                ;;
            down )
                compose_prod down -v
                ;;
            logs )
                if [ -n "${3:-}" ]; then
                    compose_prod logs -f "$3"
                else
                    compose_prod logs -f
                fi
                ;;
            * )
                usage
                ;;
        esac
        ;;
    manage )
        shift
        bootstrap
        compose_dev run --rm web python manage.py "$@"
        ;;
    test )
        bootstrap
        compose_dev run --rm web python manage.py test
        ;;
    * )
        usage
        ;;
esac

exit 0
