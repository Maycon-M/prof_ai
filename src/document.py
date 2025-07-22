from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Document:
    text: str
    embedding: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


