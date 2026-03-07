# gateway may not have domain models initially

from dataclasses import dataclass

@dataclass
class BaseEntity:
    id: int
