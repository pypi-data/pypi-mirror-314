from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from envix.pattern import DOLLAR_ENVNAME_PATTERN, ENVNAME_PATTERN

from ._common import OverwriteType


class LocalEnvsV1(BaseModel):
    """
    Local environment variables to be read from the machine's user environments.
    """

    model_config = ConfigDict(extra="forbid")

    type: Annotated[
        Literal["Local"],
        Field(
            title="Local environment variables.",
            description="Environment variables to be read from the local machine user environments.",
        ),
    ]
    items: Annotated[
        dict[
            Annotated[
                str,
                Field(pattern=ENVNAME_PATTERN),
            ],
            Annotated[
                str,
                Field(
                    title="Name of the environment variable whose value is to be read.",
                    pattern=DOLLAR_ENVNAME_PATTERN,
                ),
            ],
        ]
        | list[Annotated[str, Field(pattern=ENVNAME_PATTERN)]],
        Field(title="List of environment variable names to be read from local."),
    ]

    overwrite: OverwriteType = True

    @property
    def _items(self) -> dict[str, str]:
        if isinstance(self.items, list):
            return {envname: envname for envname in self.items}

        else:
            return {
                envname: envvar.strip("$") for envname, envvar in self.items.items()
            }
