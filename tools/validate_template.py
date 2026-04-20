from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


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
        env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")

        run(["docker", "compose", "-f", "docker/docker-compose.dev.yaml", "--env-file", ".env", "config"], cwd=project_dir)
        run(["docker", "compose", "-f", "docker/docker-compose.prd.yaml", "--env-file", ".env", "config"], cwd=project_dir)

        print(f"Template validation succeeded: {project_dir}")


if __name__ == "__main__":
    main()
