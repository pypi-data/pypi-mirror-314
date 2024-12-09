class Stdout:
    def __repr__(self) -> str:
        return "stdout"


class AutoSearch:
    def __repr__(self) -> str:
        return "auto search"


STDOUT = Stdout()
AUTO_SEARCH = AutoSearch()
