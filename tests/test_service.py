import uuid
from io import StringIO

import pandas as pd
import pytest

from app.dao.frame import Frame, Image
from app.image_processing.formatting import ImageProcessor
from app.repository.abc import ABCRepository
from app.service.frame_service import Service


class MockRepository(ABCRepository):
    def __init__(self, dataset: str) -> None:
        self.dataset = pd.read_csv(StringIO(dataset))
        self.images = [Image(id=uuid.uuid4()), Image(id=uuid.uuid4()), Image(id=uuid.uuid4())]

    async def get_frames(
        self, depth_min: float, depth_max: float, image_id: uuid.UUID
    ) -> list[Frame]:
        filtered_dataset = self.dataset[
            (self.dataset["depth"] >= depth_min) & (self.dataset["depth"] <= depth_max)
        ]
        filtered_dataset = filtered_dataset.values.tolist()
        return [
            Frame(id=uuid.uuid4(), image_id=image_id, depth=i[0], points=i[1:])
            for i in filtered_dataset
        ]

    async def get_images(self) -> list[Image]:
        return self.images


class TestService:
    @pytest.fixture
    def string_data(self):
        with open("tests/test_dataset.csv") as f:
            yield f.read()

    @pytest.fixture
    def repository(self, string_data):
        yield MockRepository(string_data)

    @pytest.fixture
    def service(self, repository):
        yield Service(repository, ImageProcessor())

    @pytest.mark.parametrize(
        "depth_min,depth_max",
        [
            [9000.2, 9000.9],
            [9000.1, 9100.0],
            [100.1, 9000.9],
            [100.1, 200.9],
        ],
        ids=[
            "in the range",
            "only the first in the range",
            "only the last in the range",
            "nothing in the range",
        ],
    )
    async def test_get_list_of_frames_filtered_by_depth(
        self, service, repository, depth_min, depth_max
    ):
        image_id = uuid.uuid4()
        repo_frames = await repository.get_frames(depth_min, depth_max, image_id)
        service_frames = await service.get_frames(depth_min, depth_max, image_id)

        for i, frame in enumerate(service_frames):
            # same response as from database, no custom color map
            assert frame.points == repo_frames[i].points

    @pytest.mark.parametrize(
        "custom_color",
        [
            "jet",
        ],
    )
    async def test_get_list_of_frames_custom_color_map(self, service, repository, custom_color):
        image_id = uuid.uuid4()
        repo_frames = await repository.get_frames(9000.2, 9000.9, image_id)
        service_frames = await service.get_frames(
            9000.2, 9000.9, image_id, custom_color=custom_color
        )

        # custom color map was applied
        for i, frame in enumerate(service_frames):
            assert frame.points != repo_frames[i].points

    async def test_get_images(self, service, repository):
        images = await service.get_images()
        assert images == await repository.get_images()
