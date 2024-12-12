from typing import Optional

import tkinter as tk
from widget_state import DictState, HigherOrderState, IntState, StringState

from ...state import PointState
from ...decorator import stateful
from .lib import CanvasItem


class LineData(HigherOrderState):

    def __init__(self, start: PointState, end: PointState):
        super().__init__()

        self.start = start
        self.end = end


class LineStyle(DictState):
    def __init__(
        self,
        color: Optional[str | StringState] = None,
        width: Optional[int | IntState] = None,
    ):
        super().__init__()

        self.color = color if isinstance(color, StringState) else StringState(color)
        self.width = width if isinstance(width, IntState) else IntState(width)


class LineState(HigherOrderState):
    def __init__(
        self,
        data: LineData,
        style: Optional[LineStyle] = None,
    ):
        super().__init__()

        self.data = data
        self.style = style if style is not None else LineStyle()


@stateful
class Line(CanvasItem):
    def __init__(self, canvas: tk.Canvas, state: LineState):
        super().__init__(canvas, state)

        self.id = None

    def draw(self, state: LineState):
        if self.id is None:
            self.id = self.canvas.create_line(
                *state.data.start.values(), *state.data.end.values()
            )

        self.canvas.coords(
            self.id, *state.data.start.values(), *state.data.end.values()
        )
        self.canvas.itemconfig(
            self.id, fill=state.style.color.value, width=state.style.width.value
        )


__all__ = ["Line", "LineData", "LineState", "LineStyle"]
