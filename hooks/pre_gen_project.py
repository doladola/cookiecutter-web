import re
import sys


def require_non_empty(name: str, value: str) -> None:
    if not value or len(value.strip()) <= 1:
        print(f"错误：'{name}' 不能为空，并且长度必须大于 1。")
        sys.exit(1)


def validate_project_slug(value: str) -> None:
    if not re.match(r"^[a-z][a-z0-9_]*$", value):
        print("错误：项目名称只能包含小写字母、数字和下划线，并且必须以字母开头。")
        sys.exit(1)


def validate_email(value: str) -> None:
    if "@" not in value or value.startswith("@") or value.endswith("@"):
        print("错误：email 字段格式不正确。")
        sys.exit(1)


project = "{{ cookiecutter.project }}"
author = "{{ cookiecutter.author }}"
email = "{{ cookiecutter.email }}"

require_non_empty("project", project)
require_non_empty("author", author)
require_non_empty("email", email)

validate_project_slug(project)
validate_email(email)

assert "\\" not in author, "错误：author 字段包含非法字符。"
