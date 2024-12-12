import json
import os
import shutil

import pytest
from pydantic import ValidationError

from ptools_base.tool import ASSERT_PATH_KEY, EXTRACT_PATH_KEY, ENV_PATH_KEY, write_asserts, copy_2_extra, write_envs
from ptools_base.schema import AssertSchema, AssertSchemaResultEnum, EnvSchema

ASSERT_FILE = 'assert.json'
EXTRA_FILE = 'extra_test_file.txt'
EXTRA_DIR = 'extra_test_dir'
EXTRA_DST_PATH = 'extra'
ENV_FILE = 'env.json'
os.environ[ASSERT_PATH_KEY] = ASSERT_FILE
os.environ[EXTRACT_PATH_KEY] = EXTRA_DST_PATH
os.environ[ENV_PATH_KEY] = ENV_FILE


class TestBaseLib:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        os.mkdir(EXTRA_DST_PATH)
        yield
        os.path.exists(ASSERT_FILE) and os.remove(ASSERT_FILE)
        shutil.rmtree(EXTRA_DST_PATH)
        os.path.exists(ENV_FILE) and os.remove(ENV_FILE)

    @pytest.fixture(autouse=True)
    def setup_method(self):
        pass
        yield
        os.path.exists(ASSERT_FILE) and os.remove(ASSERT_FILE)
        os.path.exists(ENV_FILE) and os.remove(ENV_FILE)

    @pytest.mark.parametrize("result, content, should_raise", [
        (AssertSchemaResultEnum.SUCCESS, "This is a content info", False),
        (AssertSchemaResultEnum.SUCCESS.value, "This is a content info", False),
        (AssertSchemaResultEnum.FAILED, "This is a content info", False),
        (AssertSchemaResultEnum.FAILED.value, "This is a content info", False),
        (AssertSchemaResultEnum.SKIPPED, "This is a content info", False),
        (AssertSchemaResultEnum.SKIPPED.value, "This is a content info", False),
        ("not support type", "This is a content info", True),
        (AssertSchemaResultEnum.SUCCESS, "中文字符", False),
        (None, "This is a content info", True),
        (AssertSchemaResultEnum.SUCCESS, None, True),
        (AssertSchemaResultEnum.SUCCESS, 123, True),
    ])
    def test_write_assert(self, result, content, should_raise):
        if should_raise:
            with pytest.raises(ValidationError):
                write_asserts([AssertSchema(result=result, content=content)])
        else:
            write_asserts([AssertSchema(result=result, content=content)])
            assert os.path.exists(ASSERT_FILE)
            with open(ASSERT_FILE, 'r') as file:
                data = json.load(file)
                assert [{
                    "result": result.value if isinstance(result, AssertSchemaResultEnum) else result,
                    "content": content
                }] == data

    @pytest.mark.parametrize("src, dst, should_raise", [
        (EXTRA_FILE, os.path.join(EXTRA_DST_PATH, EXTRA_FILE), False),
        (EXTRA_DIR, os.path.join(EXTRA_DST_PATH, EXTRA_DIR), False),
        ('some path not exist', False, False),
    ])
    def test_copy_2_extra(self, src, dst, should_raise):
        if should_raise:
            with pytest.raises(Exception):
                copy_2_extra(src)
        else:
            assert copy_2_extra(src) == dst

    @pytest.mark.parametrize("key, value, should_raise", [
        ("key", "value", False),
        (123, "value", True),
        (None, "value", True),
        ("key", 123, True),
        ("key", None, True),
    ])
    def test_write_envs(self, key, value, should_raise):
        if should_raise:
            with pytest.raises(ValidationError):
                write_envs([EnvSchema(key=key, value=value)])
        else:
            write_envs([EnvSchema(key=key, value=value)])
            assert os.path.exists(ENV_FILE)
            with open(ENV_FILE, 'r') as file:
                data = json.load(file)
                assert {key: value} == data
