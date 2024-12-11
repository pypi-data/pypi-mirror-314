import tkinter as tk
from typing import Optional

from widget_state import HigherOrderState, IntState

from ...state import BoundingBoxState as BoundingBoxData
from .line import Line, LineState, LineStyle, LineData
from .rectangle import Rectangle, RectangleState, RectangleStyle, RectangleData


class BoundingBoxStyle(HigherOrderState):

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


class BoundingBoxState(HigherOrderState):
    def __init__(self, data: BoundingBoxData, style: Optional[BoundingBoxStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else BoundingBoxStyle()


class BoundingBox:

    def __init__(self, canvas: tk.Canvas, state: BoundingBoxState):
        self.canvas = canvas
        self._state = state

        self.lines = []
        self.rectangles = []

        self.draw(self._state)

    def draw(self, state: BoundingBoxState):
        point_pairs = [
            (state.data.top_left(), state.data.top_right()),
            (state.data.top_left(), state.data.bottom_left()),
            (state.data.bottom_left(), state.data.bottom_right()),
            (state.data.bottom_right(), state.data.top_right()),
        ]
        self.lines.extend(
            [
                Line(
                    self.canvas,
                    LineState(LineData(start, end), style=state.style.line_style),
                )
                for start, end in point_pairs
            ]
        )

        points = [
            state.data.top_left(),
            state.data.top_right(),
            state.data.bottom_left(),
            state.data.bottom_right(),
        ]
        self.rectangles = [
            Rectangle(
                self.canvas,
                RectangleState(
                    data=RectangleData(point, size=state.style.rectangle_size),
                    style=state.style.rectangle_style,
                ),
            )
            for point in points
        ]

    def delete(self) -> None:
        for line in self.lines.values():
            line.delete()

        for rectangle in self.rectangles.values():
            rectangle.delete()


__all__ = ["BoundingBox", "BoundingBoxData", "BoundingBoxStyle", "BoundingBoxState"]
