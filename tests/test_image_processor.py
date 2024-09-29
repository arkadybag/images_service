import uuid

import matplotlib.cm as cm
import numpy as np
import pytest
from matplotlib import pyplot as plt

from app.dao.frame import Frame
from app.image_processing.formatting import ImageProcessor


class TestImageProcessor:
    @pytest.fixture
    def frame(self):
        yield Frame(
            id=uuid.uuid4(), image_id=uuid.uuid4(), depth=1.0, points=[225, 181, 170, 174, 180, 178]
        )

    @pytest.mark.parametrize(
        "color",
        [
            "jet",
        ],
    )
    def test_process_frame(self, frame, color):
        processed_frame = ImageProcessor().process_frame(frame, color)

        vector = np.array(frame.points)
        norm = plt.Normalize(vmin=vector.min(), vmax=vector.max())
        cmap = getattr(cm, color)
        colored_image = cmap(norm(vector)).tolist()

        assert colored_image == processed_frame.points

    def test_process_frame_no_color(self, frame):
        processed_frame = ImageProcessor().process_frame(frame, None)
        assert processed_frame.points == frame.points
