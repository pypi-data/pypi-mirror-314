from typing import Callable, Literal, Optional

import tkinter as tk
from widget_state import HigherOrderState, IntState

from ...decorator import stateful
from ...state import ContourState as ContourData

from .lib import CanvasItem
from .line import Line, LineState, LineData, LineStyle
from .rectangle import Rectangle, RectangleState, RectangleData, RectangleStyle


class ContourStyle(HigherOrderState):

    def __init__(
        self,
        rectangle_style: Optional[RectangleStyle] = None,
        rectangle_size: int | IntState = 10,
        line_style: Optional[LineStyle] = None,
    ):
        super().__init__()

        self.rectangle_style = (
            rectangle_style if rectangle_style is not None else RectangleStyle()
        )
        self.rectangle_size = (
            rectangle_size
            if isinstance(rectangle_size, IntState)
            else IntState(rectangle_size)
        )
        self.line_style = line_style if line_style is not None else LineStyle()


class ContourState(HigherOrderState):

    def __init__(self, data: ContourData, style: Optional[ContourStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else ContourStyle()


@stateful
class Contour:

    def __init__(self, canvas: tk.Canvas, state: ContourState):
        self.canvas = canvas
        self.widget = canvas

        self.rectangles = []
        self.lines = []

        self.bindings_rectangle = {}
        self.bindings_line = {}

    def draw(self, state: ContourState):
        self.clear()

        if len(state.data) == 0:
            return

        for start, end in zip(state.data, [*state.data[1:], state.data[0]]):
            self.lines.append(
                Line(
                    self.canvas,
                    LineState(
                        data=LineData(start=start, end=end),
                        style=state.style.line_style,
                    ),
                )
            )
            for binding, callback in self.bindings_line.items():
                self.lines[-1].tag_bind(binding, callback)

        for point in state.data:
            self.rectangles.append(
                Rectangle(
                    self.canvas,
                    RectangleState(
                        data=RectangleData(point, state.style.rectangle_size),
                        style=state.style.rectangle_style,
                    ),
                )
            )
            for binding, callback in self.bindings_rectangle.items():
                self.rectangles[-1].tag_bind(binding, callback)

    def clear(self):
        for line in self.lines:
            line.delete()
        self.lines.clear()

        for rectangle in self.rectangles:
            rectangle.delete()
        self.rectangles.clear()

    def tag_bind(
        self,
        binding: str,
        callback: Callable[[tk.Event, CanvasItem], None],
        _type: Literal["rectangle", "line"],
    ) -> None:
        bindings = (
            self.bindings_rectangle if _type == "rectangle" else self.bindings_line
        )
        bindings[binding] = callback
        self.draw(self._state)

    def delete(self):
        self.clear()

        self.bindings_rectangle.clear()
        self.bindings_line.clear()


__all__ = ["Contour", "ContourState", "ContourData", "ContourStyle"]
