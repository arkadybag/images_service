import matplotlib.cm as cm
import numpy as np
from matplotlib import pyplot as plt

from app.dao.frame import Frame


class ImageProcessor:
    color_map = {
        "jet": cm.jet,
    }

    def process_frame(self, frame: Frame, color: str | None) -> Frame:
        if not color:
            return frame

        vector = np.array(frame.points)
        norm = plt.Normalize(vmin=vector.min(), vmax=vector.max())
        color_map = self.color_map[color]
        points = color_map(norm(vector)).tolist()

        return Frame(
            id=frame.id,
            image_id=frame.image_id,
            depth=frame.depth,
            points=points,
        )
