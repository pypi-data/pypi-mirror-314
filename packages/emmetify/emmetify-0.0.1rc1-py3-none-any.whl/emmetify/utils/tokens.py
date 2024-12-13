from emmetify.data import load_single_token_names

class SingleTokenNames:
    """List of english first names that are single tokens in most LLMs."""

    def __init__(self):
        self._names: set[str] = set(load_single_token_names())

    def get_name(self) -> str:
        return self._names.pop()
