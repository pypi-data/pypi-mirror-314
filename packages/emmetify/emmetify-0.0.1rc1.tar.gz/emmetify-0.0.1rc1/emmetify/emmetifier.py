from emmetify.config import EmmetifierConfig
from emmetify.parsers import get_parser
from emmetify.converters import get_converter
from emmetify.types import SupportedFormats, DefaultFormat


class Emmetifier:
    def __init__(
        self,
        format: SupportedFormats = DefaultFormat,
        config: EmmetifierConfig | dict | None = None
    ):
        self.config = EmmetifierConfig.model_validate(config) if config else EmmetifierConfig()

        self._parser = get_parser(format, self.config)
        self._converter = get_converter(format, self.config)


    def emmetify(self, content: str) -> str:
        content_nodes = self._parser.parse(content)
        return self._converter.convert(content_nodes)

    @classmethod
    def create(cls, format: SupportedFormats = DefaultFormat, **config_kwargs) -> "Emmetifier":
        """Factory method with IDE support for config"""
        return cls(format=format, config=EmmetifierConfig(**config_kwargs))
