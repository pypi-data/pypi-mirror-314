from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from envix.pattern import ENVNAME_PATTERN

from ._common import OverwriteType


class RawEnvsV1(BaseModel):
    """
    Raw environment variables directly specified in the configuration.
    """

    model_config = ConfigDict(extra="forbid")

    type: Annotated[
        Literal["Raw"],
        Field(
            title="Raw environment variables.",
            description="Environment variable settings to be written directly in the configuration file.",
        ),
    ]

    items: Annotated[
        dict[Annotated[str, Field(pattern=ENVNAME_PATTERN)], str],
        Field(
            title="environment variable items.",
            description="A dictionary of environment variable names and values to be written directly.",
        ),
    ]

    overwrite: OverwriteType = True
