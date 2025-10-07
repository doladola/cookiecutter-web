import os
import secrets
import subprocess
import sys


def set_secret_key(length=50):
    """Generate a random secret key."""
    print("INFO: Generating SECRET_KEY...")
    secret_key = secrets.token_urlsafe(50)
    env_file_path = "docker/.env.example"
    if os.path.exists(env_file_path):
        with open(env_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("replace-with-a-secure-secret-key",secret_key,1)
        with open(env_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("INFO: SECRET_KEY updated in .env.example file.")
    else:
        print(f"WARNING: {env_file_path} not found. Skipping SECRET_KEY update.")

def create_virtualenv_and_install_dependencies():
    """Create a virtual environment and install dependencies using uv."""
    print("INFO: Creating virtual environment with uv...")
    print(subprocess.run(['uv','venv'],check=True,capture_output=True,text=True,encoding='utf-8'))
    
    print("INFO: Add dependences...")
    # 添加依赖列表
    dependences = ["django==5.2.5","gunicorn","psycopg[binary]","django-environ"]
    # 是否启动Redis缓存
    if {{ cookiecutter.use_redis }}:
        dependences.extend(['redis','hiredis'])
    # 是否使用Celery队列
    if {{ cookiecutter.use_celery }}:
        dependences.extend(['celery','django-celery-beat','redis','hiredis'])
    # 是否使用ninja
    if {{ cookiecutter.use_ninja }}:
        dependences.extend(['django-ninja'])
    # 是否使用sentry
    if {{ cookiecutter.use_sentry }}:
        dependences.extend(['sentry-sdk[django]'])
    # 依赖去重
    dependences = list(set(dependences))

    command = ['uv','add'] + dependences

    print(subprocess.run(command, check=True,capture_output=True,text=True,encoding='utf-8'))
    
    print("INFO: Virtual environment created and dependencies installed successfully.")

def initialize_git_repository():
    """Initialize a git repository."""
    print("INFO: Initializing git repository...")
    git_result = subprocess.run(["git", "init"], check=True, capture_output=True, text=True, encoding="utf-8")
    print(git_result.stdout)
    print("INFO: Git repository initialized successfully.")

def main():
    """
    Creates the virtual environment, installs dependencies, and initializes a git repository.
    """
    try:
        set_secret_key()
        create_virtualenv_and_install_dependencies()
        initialize_git_repository()
    except FileNotFoundError as e:
        print(
            f"ERROR: Command '{e.filename}' not found. Please ensure it is installed and in your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to execute command: {' '.join(e.cmd)}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
