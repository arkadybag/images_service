from uuid import UUID

from app.dao.frame import Frame, Image
from app.image_processing.formatting import ImageProcessor
from app.repository.abc import ABCRepository


class Service:
    def __init__(self, repository: ABCRepository, image_processor: ImageProcessor):
        self.repository = repository
        self.image_processor = image_processor

    async def get_frames(
        self, depth_min: float, depth_max: float, image_id: UUID, custom_color: str | None = None
    ) -> list[Frame]:
        frames = await self.repository.get_frames(depth_min, depth_max, image_id)

        processed_frames = []
        for frame in frames:
            processed_frames.append(self.image_processor.process_frame(frame, custom_color))

        return processed_frames

    async def get_images(self) -> list[Image]:
        return await self.repository.get_images()
