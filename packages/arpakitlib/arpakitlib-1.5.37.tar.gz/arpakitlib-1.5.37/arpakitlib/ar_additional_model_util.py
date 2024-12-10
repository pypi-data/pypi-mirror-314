# arpakit

from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseAM(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)
    bus_data: dict[str, Any] = {}
