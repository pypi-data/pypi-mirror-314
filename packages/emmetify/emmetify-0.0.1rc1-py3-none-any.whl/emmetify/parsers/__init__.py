from emmetify.config.base_config import EmmetifierConfig
from emmetify.nodes.base_nodes import BaseNodePool
from emmetify.parsers.base_parser import BaseParser
from emmetify.parsers.html_parser import HtmlParser
from emmetify.types import SupportedFormats, DefaultFormat


def get_parser(format: SupportedFormats, config: EmmetifierConfig) -> BaseParser[BaseNodePool]:
    parsers: dict[SupportedFormats, BaseParser[BaseNodePool]] = {
        "html": HtmlParser(config),
    }
    return parsers.get(format, parsers[DefaultFormat])
