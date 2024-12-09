import os
from pathlib import Path

from envix.envname import ENVIX_CONFIG_DIR
from envix.exception import EnvixConfigFileNotFound


def get_user_config_path(name: str, *, exist_ok=False) -> Path:
    config_path = get_registerd_config_dir().joinpath(f"envix_{name}.yml")
    if not config_path.exists() and not exist_ok:
        raise EnvixConfigFileNotFound(config_path)

    return config_path


def list_user_config() -> list[Path]:
    return list(get_registerd_config_dir().glob("envix_*.yml"))


def get_user_config_dir() -> Path:
    config_dir: Path
    if path := os.getenv(ENVIX_CONFIG_DIR):
        config_dir = Path(path)

    elif path := os.getenv("XDG_CONFIG_HOME"):
        config_dir = Path(path).joinpath("envix")

    else:
        config_dir = Path.home().joinpath(".config/envix")

    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir


def get_registerd_config_dir() -> Path:
    registerd_config_dir = get_user_config_dir().joinpath("registered")

    if not registerd_config_dir.exists():
        registerd_config_dir.mkdir(parents=True, exist_ok=True)

    return registerd_config_dir
