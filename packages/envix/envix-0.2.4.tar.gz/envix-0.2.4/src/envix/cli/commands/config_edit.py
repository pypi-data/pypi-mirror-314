import os
from argparse import ArgumentParser, _SubParsersAction
from logging import getLogger
from typing import Any, cast

from pydantic import BaseModel

from envix.envname import ENVIX_EDITOR

logger = getLogger(__name__)


class Args(BaseModel):
    config_name: str


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "Edit all available configurations."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "edit",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    parser.add_argument(
        "config_name",
        metavar="CONFIG_NAME",
        help="user registered setting name.",
        type=str,
    )

    parser.set_defaults(handler=lambda space: edit_user_config(Args(**vars(space))))


def edit_user_config(args: Args) -> None:
    import subprocess

    from envix.path import get_user_config_path

    config_path = get_user_config_path(args.config_name, exist_ok=True)

    editor = os.getenv(ENVIX_EDITOR, os.getenv("EDITOR", "vim"))

    if not os.path.exists(config_path) and editor == "code":
        with config_path.open("w") as f:
            f.write(
                "# yaml-language-server: $schema=https://raw.githubusercontent.com/yassun7010/envix-py/main/schemas/config.json\n"
            )

    subprocess.run([os.getenv(ENVIX_EDITOR, os.getenv("EDITOR", "vim")), config_path])
