from enum import Enum

from pydantic import Field
from pydantic.main import BaseModel


class AssertSchemaResultEnum(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class AssertSchema(BaseModel):
    result: AssertSchemaResultEnum = Field(title="校验结果")
    content: str = Field(title="校验消息")

    class Config:
        use_enum_values = True


class EnvSchema(BaseModel):
    key: str = Field(title="key")
    value: str = Field(title="value")
