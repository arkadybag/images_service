from uuid import UUID

from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: UUID


class ImagesSchema(BaseModel):
    data: list[ImageSchema]


class FrameSchema(BaseModel):
    id: UUID
    image_id: UUID
    depth: float
    points: list[list[float | int] | int]


class FramesSchema(BaseModel):
    data: list[FrameSchema]
