from argparse import ArgumentParser, _SubParsersAction
from typing import Any, cast

from pydantic import BaseModel

from envix.cli.commands import config_edit

from . import config_list, config_schema


class Args(BaseModel):
    commands: list[str]


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "Operations related to envix settings."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "config",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    subparsers = parser.add_subparsers(
        title="commands",
        metavar="COMMAND",
    )

    config_list.add_subparser(subparsers, formatter_class=parser.formatter_class)
    config_edit.add_subparser(subparsers, formatter_class=parser.formatter_class)
    config_schema.add_subparser(subparsers, formatter_class=parser.formatter_class)

    parser.set_defaults(handler=lambda _: parser.print_help())
