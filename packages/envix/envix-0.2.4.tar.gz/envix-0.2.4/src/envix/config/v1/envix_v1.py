from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class EnvixV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Annotated[Literal[1], Field(title="envix version.")]
