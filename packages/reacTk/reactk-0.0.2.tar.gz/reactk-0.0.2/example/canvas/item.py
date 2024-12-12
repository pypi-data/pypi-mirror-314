"""
Demo application that draws different items on a canvas (bounding box, circle, line and rectangle).

It also demonstrates different ways of styling an interacting with the items.
"""

from reacTk.state import PointState
from reacTk.widget.canvas.bounding_box import (
    BoundingBox,
    BoundingBoxData,
    BoundingBoxState,
)
from reacTk.widget.canvas.circle import Circle, CircleData, CircleStyle, CircleState
from reacTk.widget.canvas.line import Line, LineData, LineStyle, LineState
from reacTk.widget.canvas.rectangle import (
    Rectangle,
    RectangleData,
    RectangleStyle,
    RectangleState,
)

from .lib import App


class ItemApp(App):

    def __init__(self):
        super().__init__(1024, 1024)

        self.rectangle = Rectangle(
            self.canvas,
            RectangleState(
                data=RectangleData(center=PointState(512, 512), size=100),
                style=RectangleStyle(
                    color=None, outline_color="black", outline_width=32
                ),
            ),
        )
        self.rectangle.tag_bind(
            "<Button-1>",
            lambda event, rectangle: self.rectangle._state.style.outline_color.set(
                "red"
            ),
        )
        self.rectangle.tag_bind(
            "<Button-3>",
            lambda event, rectangle: self.rectangle._state.data.center.set(
                event.x, event.y
            ),
        )

        self.line = Line(
            self.canvas,
            LineState(
                data=LineData(start=PointState(50, 700), end=PointState(250, 800)),
                style=LineStyle(color="green", width=3),
            ),
        )

        self.circle = Circle(
            self.canvas,
            CircleState(
                data=CircleData(center=PointState(800, 900), radius=50),
                style=CircleStyle(color="green", outline_width=0),
            ),
        )

        self.bb = BoundingBox(
            self.canvas,
            BoundingBoxState(
                data=BoundingBoxData(800, 200, 1000, 300),
            ),
        )
        self.bb._state.style.rectangle_style.color.set("red")
        self.bb._state.data.x1.set(400)
        for rect in self.bb.rectangles:
            rect.tag_bind(
                "<B1-Motion>", lambda ev, rect: rect._state.data.center.set(ev.x, ev.y)
            )


if __name__ == "__main__":
    app = ItemApp()
    app.mainloop()
