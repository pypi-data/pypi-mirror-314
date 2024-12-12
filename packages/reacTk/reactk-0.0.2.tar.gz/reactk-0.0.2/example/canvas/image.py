"""
Demo application that draws images on a canvas.

It demonstrates how to move images around, how to use them as backgrounds,
and how to drawn on them (convert between image and canvas coordinates).
"""

import cv2 as cv
import numpy as np
from widget_state import BoolState, StringState

from reacTk.state import PointState
from reacTk.widget.canvas.image import (
    Image,
    ImageData,
    ImageStyle,
    ImageState,
)

from .lib import App


class ImageApp(App):

    def __init__(self):
        super().__init__(1600, 900)

        foreground_image_array = np.zeros((256, 256, 3), dtype=np.uint8)
        foreground_image_array = cv.rectangle(
            foreground_image_array,
            (10, 10, 200, 200),
            color=(255, 255, 255),
            thickness=5,
        )
        foreground_image = Image(
            self.canvas,
            ImageState(
                ImageData(foreground_image_array),
                ImageStyle(
                    position=PointState(400, 400),
                    background=BoolState(False),
                    fit=StringState("none"),
                ),
            ),
        )
        foreground_image.tag_bind(
            "<B1-Motion>",
            lambda event, image: image._state.style.position.set(event.x, event.y),
        )

        background_image_array = np.full(
            shape=(800, 800, 3), fill_value=(0, 127, 127), dtype=np.uint8
        )
        background_image_array = cv.circle(
            background_image_array,
            (200, 200),
            radius=20,
            color=(255, 255, 255),
            thickness=-1,
        )

        background_image = Image(
            self.canvas,
            ImageState(
                ImageData(background_image_array),
                style=ImageStyle(
                    background=BoolState(True), fit=StringState("contain")
                ),
            ),
        )
        background_image.tag_bind(
            "<Button-1>",
            lambda event, image: image._state.data.set(
                cv.circle(
                    image._state.data.value,
                    image.to_image(event.x, event.y),
                    10,
                    (255, 255, 255),
                    -1,
                )
            ),
        )


if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()
