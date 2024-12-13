from abc import ABC
from typing import Generic, TypeVar


class BaseNode(ABC):
    """Base class for all nodes"""

    # @abstractmethod
    # def is_root(self) -> bool:
    #     raise NotImplementedError


N = TypeVar("N", bound=BaseNode)


class BaseNodePool(ABC, Generic[N]):
    """Base class for all node pools"""

    def __init__(self):
        self._nodes: dict[str, N] = {}

    def get_root_ids(self) -> set[str]:
        raise NotImplementedError

NP = TypeVar("NP", bound=BaseNodePool)
