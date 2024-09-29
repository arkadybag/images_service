import dataclasses
from uuid import UUID


@dataclasses.dataclass(frozen=True)
class Frame:
    id: UUID
    image_id: UUID
    depth: float
    points: list[int | float] | list[list[int | float]]


@dataclasses.dataclass(frozen=True)
class Image:
    id: UUID
