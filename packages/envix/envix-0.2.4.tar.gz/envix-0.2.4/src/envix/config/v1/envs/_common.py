from typing import Annotated

from pydantic import Field

OverwriteType = Annotated[
    bool,
    Field(
        title="overwrite existing environment variables.",
        description="Whether to overwrite existing environment variables.",
    ),
]
