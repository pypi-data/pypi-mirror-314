from typing import Optional
import tkinter as tk

import cv2 as cv
import numpy as np
from numpy.typing import NDArray
from PIL import ImageTk
from PIL import Image as PILImage

from widget_state import BasicState, BoolState, HigherOrderState, StringState

from ...state import PointState
from ...decorator import stateful
from .lib import CanvasItem


UNDEFINED_POSITION = -100000


class ImageData(BasicState[NDArray]):

    def __init__(self, value: NDArray):
        super().__init__(value, verify_change=False)


class ImageStyle(HigherOrderState):

    def __init__(
        self,
        position: Optional[PointState] = None,
        background: Optional[BoolState] = None,
        fit: Optional[StringState] = None,
    ):
        super().__init__()

        self.position = (
            position
            if position is not None
            else PointState(UNDEFINED_POSITION, UNDEFINED_POSITION)
        )
        self.background = background if background is not None else BoolState(True)
        self.fit = fit if fit is not None else StringState("contain")


class ImageState(HigherOrderState):

    def __init__(
        self,
        data: ImageData,
        style: Optional[ImageStyle] = None,
    ):
        super().__init__()

        self.data = data
        self.style = style if style is not None else ImageStyle()


def img_to_tk(img: np.ndarray) -> ImageTk:
    return ImageTk.PhotoImage(PILImage.fromarray(img))


@stateful
class Image(CanvasItem):

    def __init__(self, canvas: tk.Canvas, state: ImageState):
        super().__init__(canvas, state)

        self.img_tk = None
        self.id = None

        if state.style.position.x.value == UNDEFINED_POSITION:
            state.style.position.x.value = int(canvas["width"]) // 2
        if state.style.position.y.value == UNDEFINED_POSITION:
            state.style.position.y.value = int(canvas["height"]) // 2

        self.scale_x, self.scale_y = self.compute_scales()

    def compute_scales(self):
        scale_x = int(self.canvas["width"]) / self._state.data.value.shape[1]
        scale_y = int(self.canvas["height"]) / self._state.data.value.shape[0]

        fit = self._state.style.fit.value
        if fit == "fill":
            return scale_x, scale_y
        elif fit == "contain":
            scale_x = scale_y = min(scale_x, scale_y)
            return scale_x, scale_y
        elif fit == "cover":
            scale_x = scale_y = max(scale_x, scale_y)
            return scale_x, scale_y

        scale_x = scale_y = 1.0
        return scale_x, scale_y

    def draw(self, state: ImageState) -> None:
        self.img_tk = img_to_tk(
            cv.resize(state.data.value, None, fx=self.scale_x, fy=self.scale_y)
        )

        if self.id is None:
            self.id = self.canvas.create_image(
                *state.style.position.values(), image=self.img_tk
            )

        self.canvas.coords(self.id, *state.style.position.values())
        self.canvas.itemconfig(self.id, image=self.img_tk)

        if state.style.background.value:
            self.canvas.tag_lower(self.id)

    def to_image(self, x: int, y: int) -> tuple[int, int]:
        """
        Transform x-, and y-coordinates from canvas space to image space.

        Parameters
        ----------
        x: int
        y: int

        Returns
        -------
        tuple[int, int]
        """
        image_width = self._state.data.value.shape[1]
        image_height = self._state.data.value.shape[0]

        canvas_width = int(self.canvas["width"])
        canvas_height = int(self.canvas["height"])

        t_x = (canvas_width - image_width * self.scale_x) // 2
        t_y = (canvas_height - image_height * self.scale_y) // 2

        x = round((x - t_x) / self.scale_x)
        y = round((y - t_y) / self.scale_y)
        return x, y

    def to_canvas(self, x: int, y: int) -> tuple[int, int]:
        """
        Transform x-, and y-coordinates from image space to canvas space.

        Parameters
        ----------
        x: int
        y: int

        Returns
        -------
        tuple[int, int]
        """
        image_width = self._state.data.value.shape[1]
        image_height = self._state.data.value.shape[0]

        canvas_width = int(self.canvas["width"])
        canvas_height = int(self.canvas["height"])

        t_x = (canvas_width - image_width * self.scale_x) // 2
        t_y = (canvas_height - image_height * self.scale_y) // 2

        x = round(x * self.scale_x + t_x)
        y = round(y * self.scale_y + t_y)

        return x, y
