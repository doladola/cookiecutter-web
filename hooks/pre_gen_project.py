import re
import sys


def name_check(name:str,content:str):
    if not content or len(content.strip()) <= 1:
        print(f"错误： '{name}' 字段不能为空，并且长度必须大于1。")
        sys.exit(1)


    if not re.match(r'^[a-z][a-z0-9_]*$', content):
        print(f"错误：项目名称 '{name}' 只能包含小写字母、数字和下划线，并且必须以字母开头。")
        sys.exit(1)

name_check('project','{{ cookiecutter.project }}')


assert "\\" not in "{{ cookiecutter.author }}", "用户名不合法！"

if {{ cookiecutter.use_celery }} and  not {{ cookiecutter.use_redis }}:
    print(f"错误：使用Celery需要设置`use_redis`为`True`！")
    sys.exit(1)