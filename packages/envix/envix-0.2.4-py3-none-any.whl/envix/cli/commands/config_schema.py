import json
from argparse import ArgumentParser, FileType, _SubParsersAction
from typing import IO, Any, cast

from pydantic import BaseModel, ConfigDict

from envix.config.config import Config


class Args(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    output_file: IO | None


def add_subparser(subparsers: "_SubParsersAction[Any]", **kwargs: Any) -> None:
    help = "Outputs the JSON schema of the envix config file."

    parser = cast(
        ArgumentParser,
        subparsers.add_parser(
            "schema",
            description=help,
            help=help,
            **kwargs,
        ),
    )

    parser.add_argument(
        "--output-file",
        "-o",
        metavar="OUTPUT",
        help="output file path.",
        type=FileType("w"),
        default=None,
    )

    parser.set_defaults(
        handler=lambda space: config_schema_command(Args(**vars(space)))
    )


def config_schema_command(args: Args) -> None:
    print(
        json.dumps(
            Config.model_json_schema(by_alias=True),
            indent=2,
            ensure_ascii=False,
        ),
        file=args.output_file,
    )
