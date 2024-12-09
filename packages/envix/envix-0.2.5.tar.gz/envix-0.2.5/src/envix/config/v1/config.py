from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from envix.config.v1.envix_v1 import EnvixV1

from .envs import EnvsV1


class ConfigV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    envix: Annotated[EnvixV1, Field(description="Envix settings")]
    includes: list[Path] = Field(
        description="List of envix config paths to include", default_factory=list
    )
    envs: list[EnvsV1] = Field(
        description="List of environment variables settings", default_factory=list
    )
