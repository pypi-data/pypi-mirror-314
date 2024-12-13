from abc import ABC, abstractmethod
from typing import Generic

from emmetify.nodes.base_nodes import NP
from emmetify.config.base_config import EmmetifierConfig


class BaseConverter(Generic[NP]):
    """Base interface for all converters"""

    def __init__(self, config: EmmetifierConfig):
        self.config = config

    @abstractmethod
    def _build_emmet(self, node_pool: NP, root_id: str) -> str:
        raise NotImplementedError

    def convert(self, node_pool: NP) -> str:
        root_ids = node_pool.get_root_ids()

        if not root_ids:
            return ''

        emmet_parts = []
        sorted_root_ids = sorted(root_ids)
        for i, root_id in enumerate(sorted_root_ids):
            emmet = self._build_emmet(node_pool, root_id)
            if emmet:
                if i < len(sorted_root_ids) - 1:
                    if self.config.indent:
                        emmet = f"{emmet}+\n"
                    else:
                        emmet = f"{emmet}+"
                emmet_parts.append(emmet)
        
        # Join multiple root elements
        result = ''.join(emmet_parts)

        # if self.config.debug:
            # print("\nEmmet notation:")
            # print(result)
        return result
