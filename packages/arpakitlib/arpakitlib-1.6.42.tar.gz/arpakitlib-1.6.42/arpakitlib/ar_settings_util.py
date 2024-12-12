from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings

from arpakitlib.ar_enumeration_util import Enumeration


class ModeTypes(Enumeration):
    local: str = "local"
    dev: str = "dev"
    preprod: str = "preprod"
    prod: str = "prod"


class SimpleSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    mode_type: str

    @field_validator("mode_type")
    @classmethod
    def validate_mode_type(cls, v: str):
        ModeTypes.parse_and_validate_values(v)
        return v
