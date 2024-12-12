from typing import Optional

import tkinter as tk
from widget_state import DictState, HigherOrderState, IntState, StringState

from ...state import PointState
from ...decorator import stateful
from .lib import CanvasItem


class RectangleStyle(DictState):

    def __init__(
        self,
        color: Optional[str | StringState] = None,
        outline_color: Optional[str | StringState] = None,
        outline_width: Optional[int | IntState] = None,
    ):
        super().__init__()

        self.color = color if isinstance(color, StringState) else StringState(color)
        self.outline_color = (
            outline_color
            if isinstance(outline_color, StringState)
            else StringState(outline_color)
        )
        self.outline_width = (
            outline_width
            if isinstance(outline_width, IntState)
            else IntState(outline_width)
        )


class RectangleData(HigherOrderState):

    def __init__(self, center: PointState, size: int):
        super().__init__()

        self.center = center
        self.size = size

    def ltbr(self):
        size_h = self.size.value // 2
        x, y = self.center.values()
        return [
            x - size_h,
            y - size_h,
            x + size_h,
            y + size_h,
        ]


class RectangleState(HigherOrderState):

    def __init__(self, data: RectangleData, style: Optional[RectangleStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else RectangleStyle()


@stateful
class Rectangle(CanvasItem):
    def __init__(self, canvas: tk.Canvas, state: RectangleState):
        super().__init__(canvas, state)

        self.id = None

    def draw(self, state: RectangleState):
        if self.id is None:
            self.id = self.canvas.create_rectangle(*state.data.ltbr())

        self.canvas.coords(self.id, *state.data.ltbr())
        self.canvas.itemconfig(
            self.id,
            fill=state.style.color.value,
            outline=state.style.outline_color.value,
            width=state.style.outline_width.value,
        )
