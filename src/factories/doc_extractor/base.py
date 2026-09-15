from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class DocumentChunk:
    content: str
    type: str
    level: int = 0
    page: int = 0
    metadata: dict = field(default_factory=dict)

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, path: str) -> list[DocumentChunk]:
        pass