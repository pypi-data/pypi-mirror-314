from abc import ABC, abstractmethod
from typing import Generic

from emmetify.config.base_config import EmmetifierConfig
from emmetify.nodes.base_nodes import NP


class BaseParser(Generic[NP], ABC):
    def __init__(self, config: EmmetifierConfig):
        self.config = config

    @abstractmethod
    def parse(self, content: str) -> NP:
        raise NotImplementedError
