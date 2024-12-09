import asyncio
import json
from argparse import ArgumentParser, FileType, _SubParsersAction
from io import TextIOWrapper
from pathlib import Path
from shlex import quote
from typing import Annotated, Any, Literal, assert_never, cast, get_args

from pydantic import BaseModel, ConfigDict, SecretStr

from envix.cli.default import AUTO_SEARCH, STDOUT
from envix.cli.field import ConfigFileValidator, OutputFileValidator

OutputFormat = Literal[
    "dotenv",
    "json",
    "export-posix-shell",
]


class Args(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config_file: Annotated[Path | None, ConfigFileValidator]
    config_name: list[str] | None
    output_file: Annotated[TextIOWrapper | None, OutputFileValidator]
    format: OutputFormat
    dotenv: list[Path] | None


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "Output environment variables to a file."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "export",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    parser.add_argument(
        "--config-file",
        "--file",
        metavar="CONFIG_FILE",
        help="config file path.",
        type=Path,
        default=AUTO_SEARCH,
    )

    parser.add_argument(
        "--config-name",
        "--config",
        metavar="CONFIG_NAME",
        help="user registered setting name.",
        type=str,
        nargs="*",
    )

    parser.add_argument(
        "--output-file",
        "-o",
        help="output file path.",
        type=FileType("w"),
        default=STDOUT,
    )

    parser.add_argument(
        "--format",
        help="output format.",
        choices=get_args(OutputFormat),
        default="dotenv",
    )

    parser.add_argument(
        "--dotenv",
        metavar="DOTENV",
        help="Path to the .env file.",
        type=Path,
        default=None,
        nargs="*",
    )

    parser.set_defaults(handler=lambda space: export_command(Args(**vars(space))))


def export_command(args: Args) -> None:
    from dotenv.main import DotEnv

    from envix.config.config import collect_config_filepaths
    from envix.exception import (
        EnvixLoadEnvsError,
    )
    from envix.loader import load_secrets

    secrets, errors = asyncio.run(
        load_secrets(collect_config_filepaths(args.config_file, args.config_name))
    )

    if args.dotenv == []:
        args.dotenv = [Path(".env")]

    for dotenv in args.dotenv or []:
        for key, value in DotEnv(dotenv, override=True).dict().items():
            if value:
                secrets[key] = SecretStr(value)

    if errors:
        raise EnvixLoadEnvsError(errors)

    match args.format:
        case "dotenv":
            print(
                "\n".join(
                    f"{envname}={quote(secret.get_secret_value())}"
                    for envname, secret in secrets.items()
                ),
                file=args.output_file,
            )

        case "json":
            print(
                json.dumps(
                    {
                        envname: secret.get_secret_value()
                        for envname, secret in secrets.items()
                    }
                ),
                file=args.output_file,
            )

        case "export-posix-shell":
            print(
                "\n".join(
                    f'export {envname}="{quote(secret.get_secret_value())}"'
                    for envname, secret in secrets.items()
                ),
                file=args.output_file,
            )

        case _:
            assert_never(args.format)
