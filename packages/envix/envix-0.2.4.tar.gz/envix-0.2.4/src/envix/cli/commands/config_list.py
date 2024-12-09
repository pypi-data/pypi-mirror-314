from argparse import ArgumentParser, _SubParsersAction
from logging import getLogger
from typing import Any, cast

from pydantic import BaseModel

logger = getLogger(__name__)


class Args(BaseModel):
    commands: list[str]


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "List all available configurations."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "list",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    parser.set_defaults(handler=lambda _: list_user_config())


def list_user_config() -> None:
    from envix.path import list_user_config

    configs = list_user_config()

    if configs:
        for config in configs:
            print(config.name.lstrip("envix_").rstrip(".yml"))
    else:
        logger.info("No configurations found.")
