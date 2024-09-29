from uuid import UUID

from app.dao.frame import Frame, Image


class ABCRepository:
    async def get_frames(self, depth_min: float, depth_max: float, image_id: UUID) -> list[Frame]:
        raise NotImplementedError

    async def get_images(self) -> list[Image]:
        raise NotImplementedError
