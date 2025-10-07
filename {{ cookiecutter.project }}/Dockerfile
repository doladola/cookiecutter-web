FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://mirrors.bfsu.edu.cn/pypi/web/simple -r requirements.txt

# 设置环境变量
ENV DEBUG=False

# 创建项目目录
RUN mkdir -p /app/log /app/static /app/media

# 复制项目文件
COPY . .

# 赋予入口脚本执行权限
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# 使用入口脚本启动（包含自动迁移及管理员账号创建）
ENTRYPOINT ["/app/entrypoint.sh"]
