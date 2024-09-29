from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.dao.frame import Frame, Image
from app.repository.abc import ABCRepository
from app.sqlmodel.models import Frame as SQLFrame
from app.sqlmodel.models import Image as SQLImage


class SQLRepository(ABCRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_manager = session_factory

    async def get_frames(self, depth_min: float, depth_max: float, image_id: UUID) -> list[Frame]:
        async with self.session_manager() as session:
            frames = (
                await session.execute(
                    select(SQLFrame)
                    .where(
                        and_(
                            SQLFrame.image_id == image_id,
                            SQLFrame.depth >= depth_min,
                            SQLFrame.depth <= depth_max,
                        )
                    )
                    .order_by(SQLFrame.depth)
                )
            ).scalars()

        return [
            Frame(id=frame.id, image_id=frame.image_id, depth=frame.depth, points=frame.points)
            for frame in frames
        ]

    async def get_images(self) -> list[Image]:
        async with self.session_manager() as session:
            sqlimages = (await session.execute(select(SQLImage))).scalars().all()

        return [Image(id=i.id) for i in sqlimages]
