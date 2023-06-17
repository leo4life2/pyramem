from abc import ABC, abstractmethod
from typing import List, Optional, Any

class AbstractDatastore(ABC):
    
    @abstractmethod
    def __init__(self, name: str):
        pass

    @abstractmethod
    def upsertOne(self, vector_id: str, vector: List[float], text: str, metadata: Optional[Any] = None) -> bool:
        pass

    @abstractmethod
    def query(self, vector: Any, top_k: int = 10, include_values: bool = False, include_metadata: bool = True) -> Any:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass