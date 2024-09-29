import csv
import uuid

import pytest
from sqlalchemy import select

from app.repository.sql_repository import SQLRepository
from app.sqlmodel.models import Frame as SQLFrame
from app.sqlmodel.models import Image as SQLImage


class TestSQLRepository:
    image_id = uuid.uuid4()

    @pytest.fixture
    def string_data(self):
        with open("tests/test_dataset.csv") as f:
            reader = csv.reader(f)
            data = list(reader)
        yield data

    @pytest.fixture
    async def populate_data(self, session_factory, string_data):
        async with session_factory.begin() as session:
            image = SQLImage(id=self.image_id)
            session.add(image)
            await session.flush()

            frames = [
                SQLFrame(image_id=image.id, depth=float(row[0]), points=[int(i) for i in row[1:]])
                for row in string_data[1:]
            ]
            session.add_all(frames)

    @pytest.fixture
    def repository(self, session_factory):
        yield SQLRepository(session_factory)

    @pytest.mark.parametrize(
        "depth_min,depth_max,borders",
        [
            [9000.2, 9000.9, [9000.2, 9000.9]],
            [9000.1, 9100.0, [9000.1, 9002.0]],
            [100.1, 9000.9, [9000.1, 9000.9]],
            [100.1, 200.9, [None, None]],
        ],
        ids=[
            "in the range",
            "only the first in the range",
            "only the last in the range",
            "nothing in the range",
        ],
    )
    async def test_get_frames(
        self, repository, populate_data, session_factory, depth_min, depth_max, borders
    ):
        repo_frames = await repository.get_frames(depth_min, depth_max, self.image_id)

        async with session_factory() as session:
            sqlframes = (
                (
                    await session.execute(
                        select(SQLFrame)
                        .where(SQLFrame.depth >= depth_min, SQLFrame.depth <= depth_max)
                        .order_by(SQLFrame.depth)
                    )
                )
                .scalars()
                .all()
            )

        for rframe, sqlframe in zip(repo_frames, sqlframes):
            assert rframe.id == sqlframe.id

        assert len(repo_frames) == len(sqlframes)
        if borders[0]:
            assert repo_frames[0].depth == borders[0]
        else:
            assert not repo_frames

        if borders[1]:
            assert repo_frames[-1].depth == borders[1]
        else:
            assert not repo_frames

    async def test_get_images(self, repository, populate_data, session_factory):
        images = await repository.get_images()

        async with session_factory() as session:
            sqlimages = (await session.execute(select(SQLImage))).scalars().all()

        assert len(images) == len(sqlimages) == 1

        for rimage, sqlimage in zip(images, sqlimages):
            assert rimage.id == sqlimage.id
