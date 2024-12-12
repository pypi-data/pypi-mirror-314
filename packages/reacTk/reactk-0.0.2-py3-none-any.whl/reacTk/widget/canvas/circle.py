from typing import Optional
import tkinter as tk

from widget_state import DictState, HigherOrderState, StringState, IntState

from ...state import PointState
from ...decorator import stateful
from .lib import CanvasItem


class CircleStyle(DictState):

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


class CircleData(HigherOrderState):

    def __init__(self, center: PointState, radius: int):
        super().__init__()

        self.center = center
        self.radius = radius

    def ltbr(self):
        radius = self.radius.value
        cx, cy = self.center.values()
        return [
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
        ]


class CircleState(HigherOrderState):

    def __init__(self, data: CircleData, style: Optional[CircleStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else CircleStyle()


@stateful
class Circle(CanvasItem):

    def __init__(self, canvas: tk.Canvas, state: CircleState):
        super().__init__(canvas, state)

        self.id = None

    def draw(self, state: CircleState):
        if self.id is None:
            self.id = self.canvas.create_oval(*state.data.ltbr())

        self.canvas.coords(self.id, *state.data.ltbr())
        self.canvas.itemconfig(
            self.id,
            fill=state.style.color.value,
            outline=state.style.outline_color.value,
            width=state.style.outline_width.value,
        )
