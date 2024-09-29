from typing import Any

import cv2
import numpy as np
from numpy import ndarray

from app.resource.database import create_session_manager
from app.sqlmodel.models import Frame, Image
from settings import Settings


async def import_data(settings: Settings, rows: list[list[str]]) -> None:
    session_manager = create_session_manager(settings)

    vectors = resize_input(rows)

    async with session_manager.begin() as session:
        image = Image()
        session.add(image)
        await session.flush()

        frames_data = [
            Frame(image_id=image.id, depth=i["depth"], points=i["vector"]) for i in vectors
        ]

        session.add_all(frames_data)


def resize_input(rows: list[list[str]]) -> list[dict[str, ndarray[Any, Any] | float]]:
    resized_vectors = []

    for row in rows:
        vector = np.array(row[1:], dtype=np.uint8)
        resized_vector = cv2.resize(
            vector.reshape(1, -1), (150, 1), interpolation=cv2.INTER_LINEAR
        ).flatten()
        resized_vectors.append({"depth": float(row[0]), "vector": resized_vector})

    return resized_vectors
