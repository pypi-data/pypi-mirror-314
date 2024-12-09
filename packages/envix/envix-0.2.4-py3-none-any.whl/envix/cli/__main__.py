from logging import getLogger

from envix.cli import App
from envix.exception import EnvixLoadEnvsError

logger = getLogger(__name__)


def main() -> None:
    try:
        App.run()

    except EnvixLoadEnvsError as e:
        for error in e.errors:
            logger.error(error)
        exit(1)

    except Exception:
        exit(1)


if __name__ == "__main__":
    main()
