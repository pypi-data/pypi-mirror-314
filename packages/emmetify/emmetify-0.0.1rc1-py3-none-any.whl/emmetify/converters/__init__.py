
from typing import Dict
from emmetify.config.base_config import EmmetifierConfig
from emmetify.converters.base_converter import BaseConverter
from emmetify.converters.html_converter import HtmlConverter
from emmetify.nodes.base_nodes import BaseNodePool
from emmetify.types import SupportedFormats, DefaultFormat


def get_converter(format: SupportedFormats, config: EmmetifierConfig) -> BaseConverter[BaseNodePool]:
    converters: Dict[SupportedFormats, BaseConverter[BaseNodePool]] = {
        "html": HtmlConverter(config),
    }
    return converters.get(format, converters[DefaultFormat])
