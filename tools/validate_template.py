from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent
VALIDATE_APP_PORT = "18080"


def run(command: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    if result.stdout:
        print(result.stdout.strip())


def run_allow_failure(command: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"Cleanup command failed ({result.returncode}): {' '.join(command)}", file=sys.stderr)


def ensure_files_exist(project_dir: Path) -> None:
    required = [
        project_dir / "requirements.txt",
        project_dir / "Dockerfile",
        project_dir / "entrypoint.sh",
        project_dir / ".env.example",
        project_dir / "docker" / "docker-compose.dev.yaml",
        project_dir / "docker" / "docker-compose.prd.yaml",
        project_dir / "docker" / "nginx.conf",
        project_dir / project_dir.name / "settings.py",
        project_dir / project_dir.name / "celery.py",
        project_dir / "core" / "views.py",
        project_dir / "core" / "templates" / "base.html",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing expected files:\n" + "\n".join(missing))


def wait_for_http(url: str, expected: str, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None

    while time.time() < deadline:
        try:
            with urlopen(url, timeout=5) as response:
                body = response.read().decode("utf-8")
            if expected in body:
                return
            last_error = RuntimeError(f"Expected '{expected}' in response from {url}.")
        except URLError as exc:
            last_error = exc
        time.sleep(2)

    raise SystemExit(f"HTTP smoke check failed for {url}: {last_error}")


def main() -> None:
    if not shutil.which("uvx"):
        raise SystemExit("uvx is required to validate the template.")
    if not shutil.which("docker"):
        raise SystemExit("docker is required to validate docker compose files.")

    with tempfile.TemporaryDirectory(prefix="cookiecutter-web-") as tmp:
        output_dir = Path(tmp)
        run(
            [
                "uvx",
                "cookiecutter",
                str(ROOT),
                "--no-input",
                "--output-dir",
                str(output_dir),
                "project=demo_project",
                "description=Demo project",
                "author=Copilot",
                "email=copilot@example.com",
                "timezone=UTC",
                "language=en-us",
            ]
        )

        project_dir = output_dir / "demo_project"
        ensure_files_exist(project_dir)
        env_example = project_dir / ".env.example"
        env_file = project_dir / ".env"
        env_contents = env_example.read_text(encoding="utf-8").replace("APP_PORT=8000", f"APP_PORT={VALIDATE_APP_PORT}")
        env_file.write_text(env_contents, encoding="utf-8")

        dev_compose = ["docker", "compose", "-f", "docker/docker-compose.dev.yaml", "--env-file", ".env"]
        prod_compose = ["docker", "compose", "-f", "docker/docker-compose.prd.yaml", "--env-file", ".env"]

        run(dev_compose + ["config"], cwd=project_dir)
        run(prod_compose + ["config"], cwd=project_dir)

        try:
            run(dev_compose + ["up", "--build", "-d", "db", "redis", "celery-worker", "celery-beat"], cwd=project_dir)
            run(dev_compose + ["run", "--rm", "web", "python", "manage.py", "check"], cwd=project_dir)
            run(dev_compose + ["run", "--rm", "web", "python", "manage.py", "test"], cwd=project_dir)
            run(dev_compose + ["run", "--rm", "web", "python", "manage.py", "verify_stack", "--timeout", "30"], cwd=project_dir)
            run(dev_compose + ["up", "-d", "web"], cwd=project_dir)

            wait_for_http(f"http://127.0.0.1:{VALIDATE_APP_PORT}/", "Django starter is ready")
            wait_for_http(f"http://127.0.0.1:{VALIDATE_APP_PORT}/partials/service-status/", "PostgreSQL ready")

            print(f"Template validation succeeded: {project_dir}")
        finally:
            run_allow_failure(dev_compose + ["down", "-v", "--remove-orphans"], cwd=project_dir)


if __name__ == "__main__":
    main()
