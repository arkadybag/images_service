import csv
from io import StringIO

import cv2
import numpy as np
import pytest
from sqlalchemy import select

from app.image_processing.import_data import import_data
from app.sqlmodel.models import Frame, Image


@pytest.fixture
def data():
    csv_data = """9000.1,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,225,226,225,224,223,221,220,217,217
9000.2,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,224,225,226,225,224,223,222,221,219,219
"""
    yield csv_data


async def test_import_data(session_factory, config, data):
    reader = csv.reader(StringIO(data))
    rows = list(reader)

    await import_data(config, rows)

    async with session_factory() as session:
        images = (await session.execute(select(Image))).scalars().all()
        image = images[0]

        frames = (
            (await session.execute(select(Frame).where(Frame.image_id == image.id))).scalars().all()
        )

    resized_vectors = []

    for row in rows:
        vector = np.array(row[1:], dtype=np.uint8)
        resized_vector = cv2.resize(
            vector.reshape(1, -1), (150, 1), interpolation=cv2.INTER_LINEAR
        ).flatten()

        resized_vectors.append({"depth": float(row[0]), "vector": resized_vector})

    for i, v in enumerate(resized_vectors):
        assert v["depth"] == frames[i].depth
        assert list(v["vector"]) == frames[i].points

    # we insert only one during the testing
    assert len(images) == 1
