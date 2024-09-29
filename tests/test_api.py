import csv
import uuid

import pytest

from app.sqlmodel.models import Frame as SQLFrame
from app.sqlmodel.models import Image as SQLImage


class TestAPI:
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

        yield frames

    async def test_get_images(self, client, populate_data):
        response = await client.get("/api/v1/images")
        assert response.status_code == 200
        data = response.json()

        assert data["data"][0]["id"] == str(self.image_id)
        assert len(data["data"]) == 1

    @pytest.mark.parametrize(
        "depth_min,depth_max,borders,total",
        [
            [9000.2, 9000.9, [9000.2, 9000.9], 8],
            [9000.1, 9100.0, [9000.1, 9002.0], 20],
            [100.1, 9000.9, [9000.1, 9000.9], 9],
            [100.1, 200.9, [None, None], 0],
        ],
        ids=[
            "in the range",
            "only the first in the range",
            "only the last in the range",
            "nothing in the range",
        ],
    )
    async def test_get_frames(self, client, populate_data, depth_min, depth_max, borders, total):
        resource = await client.get(
            f"/api/v1/frames/{self.image_id}",
            params={
                "depth_min": depth_min,
                "depth_max": depth_max,
            },
        )
        assert resource.status_code == 200

        data = resource.json()

        assert len(data["data"]) == total

        if borders[0]:
            assert data["data"][0]["depth"] == borders[0]
        else:
            assert not data["data"]

        if borders[1]:
            assert data["data"][-1]["depth"] == borders[1]
        else:
            assert not data["data"]

    async def test_wrong_image(self, client, populate_data):
        resource = await client.get(
            f"/api/v1/frames/{uuid.uuid4()}",
            params={
                "depth_min": 0,
                "depth_max": 10000,
            },
        )
        assert resource.status_code == 200

        data = resource.json()

        assert len(data["data"]) == 0

    @pytest.mark.parametrize(
        "color",
        [
            "jet",
        ],
    )
    async def test_custom_color(self, client, populate_data, color):
        resource = await client.get(
            f"/api/v1/frames/{self.image_id}",
            params={"depth_min": 0, "depth_max": 10000, "custom_color": color},
        )

        assert resource.status_code == 200
        data = resource.json()

        apiframes = data["data"]

        for apiimage, sqlframe in zip(apiframes, populate_data):
            assert apiimage["id"] == str(sqlframe.id)
            assert apiimage["points"] != sqlframe.points
