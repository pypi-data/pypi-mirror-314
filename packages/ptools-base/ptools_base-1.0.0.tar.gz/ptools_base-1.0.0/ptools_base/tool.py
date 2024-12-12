import json
import os
import shutil
from typing import List

from ptools_base.schema import AssertSchema, EnvSchema

ASSERT_PATH_KEY = 'ASSERT_PATH_KEY'
EXTRACT_PATH_KEY = 'EXTRACT_PATH_KEY'
ENV_PATH_KEY = 'ENV_PATH_KEY'


def write_asserts(data: List[AssertSchema]):
    """
    write asserts data
    :param data: asserts data
    """
    assert_path = os.environ.get(ASSERT_PATH_KEY)
    if assert_path:
        with open(assert_path, 'w', encoding="utf-8") as file:
            json.dump([i.model_dump() for i in data], file, ensure_ascii=False)


def copy_2_extra(src: str):
    """
    copy source to extra path, for extra upload
    :param src: source path, a file or directory
    :return extra path or False
    """
    extra_path = os.environ.get(EXTRACT_PATH_KEY)
    if extra_path:
        if os.path.exists(src):
            if os.path.isdir(src):
                return shutil.copytree(src, os.path.join(extra_path, src))
            else:
                return shutil.copy(src, extra_path)
        else:
            return False


def write_envs(env_schemas: List[EnvSchema]):
    """
    write env data to env_file
    :param env_schemas: env data
    """
    env_path = os.environ.get(ENV_PATH_KEY)
    if env_path:
        with open(env_path, 'w', encoding="utf-8") as file:
            json.dump({env_schema.key: env_schema.value for env_schema in env_schemas}, file, ensure_ascii=False)
