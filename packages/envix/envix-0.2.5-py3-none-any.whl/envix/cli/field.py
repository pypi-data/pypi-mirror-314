from io import TextIOWrapper
from pathlib import Path

from pydantic import BeforeValidator, ValidationInfo

from envix.cli.default import AutoSearch, Stdout


def validate_config_file(
    config_file: Path | AutoSearch, info: ValidationInfo
) -> Path | None:
    return None if isinstance(config_file, AutoSearch) else config_file


def validate_output_file(
    output_file: TextIOWrapper | Stdout, info: ValidationInfo
) -> TextIOWrapper | None:
    return None if isinstance(output_file, Stdout) else output_file


ConfigFileValidator = BeforeValidator(validate_config_file)
OutputFileValidator = BeforeValidator(validate_output_file)
