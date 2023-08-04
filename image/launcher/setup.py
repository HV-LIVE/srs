import os
import shutil
from typing import Dict

from jinja2 import Environment, select_autoescape, FileSystemLoader, StrictUndefined

RELEASE = os.getenv('HV_RELEASE', '') == 'true'

cleanup_files = [
    '/usr/local/srs/conf/custom.conf',
]

template_files = [
    'usr/local/srs/conf/custom.conf',
]


def load_env_vars() -> Dict[str, str]:
    result = dict()
    for env in os.environ:
        if not env.startswith('HV_'):
            continue
        key = env[len('HV_'):].upper()
        result[key] = os.environ[env]
    return result


def cleanup():
    if not RELEASE:
        return
    for file in cleanup_files:
        shutil.rmtree(file, ignore_errors=True)


def setup():
    cleanup()

    template_env = Environment(
        loader=FileSystemLoader('template'),
        autoescape=select_autoescape(),
        undefined=StrictUndefined,
        trim_blocks=True,
    )

    env_vars = load_env_vars()
    for template in template_files:
        output_file = '/' + template if RELEASE else './.debug/' + template
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        template_env.get_template(template).stream(**env_vars).dump(output_file, encoding='utf-8')


if __name__ == '__main__':
    if not RELEASE:
        print('running in debug mode')
    setup()
