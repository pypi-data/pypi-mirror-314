import asyncio
import os
from pathlib import Path
from typing import assert_never

from pydantic import ValidationError

from envix.config.config import Config
from envix.config.v1.config import ConfigV1
from envix.exception import (
    EnvixConfigFileNotFound,
    EnvixConfigFileParseError,
    EnvixEnvInjectionError,
)
from envix.loader.v1_loader import load_envs_v1
from envix.types import Secrets


async def load_secrets(
    config_filepath: Path | list[Path] | None = None,
) -> tuple[Secrets, list[EnvixEnvInjectionError]]:
    if isinstance(config_filepath, list):
        total_secrets: Secrets = {}
        total_errors: list[EnvixEnvInjectionError] = []

        results = await asyncio.gather(
            *[load_secrets(path) for path in config_filepath]
        )

        for secrets, errors in results:
            total_secrets.update(secrets)
            total_errors.extend(errors)

        return total_secrets, total_errors

    return await _load_secrets(config_filepath)


async def _load_secrets(
    config_filepath: Path | None = None,
) -> tuple[Secrets, list[EnvixEnvInjectionError]]:
    return await collect_secrets(Config.load(config_filepath), config_filepath)


async def collect_secrets(config: Config, config_filepath: Path | None):
    total_secrets: Secrets = {}
    total_errors: list[EnvixEnvInjectionError] = []

    config_root = config.root
    config_filepath = config_filepath or Path(os.getcwd())

    match config_root:
        case ConfigV1():
            for include_path in config_root.includes:
                if not include_path.is_absolute():
                    include_path = config_filepath.parent / include_path

                if include_path.exists():
                    try:
                        secrets, errors = await load_secrets(include_path)
                        total_secrets.update(secrets)
                        total_errors.extend(errors)
                    except ValidationError:
                        total_errors.append(EnvixConfigFileParseError(include_path))
                else:
                    total_errors.append(EnvixConfigFileNotFound(include_path))

            for envs in config_root.envs:
                secrets, errors = await load_envs_v1(envs)
                total_secrets.update(secrets)
                total_errors.extend(errors)

        case _:
            assert_never(config_root)

    return total_secrets, total_errors
