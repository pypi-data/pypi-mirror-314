"""
Demo application that draws a contour on a canvas.

The contour can be modified:
  * vertices can be moved by dragging them with the mouse
  * vertices can be removed on right click
  * vertices can be added by double-clicking somewhere on a line
"""

from reacTk.state import PointState
from reacTk.widget.canvas.contour import (
    Contour,
    ContourData,
    ContourState,
)

from .lib import App


class ContourApp(App):
    def __init__(self):
        super().__init__()

        contour = Contour(
            canvas=self.canvas,
            state=ContourState(
                data=ContourData(
                    [
                        PointState(100, 100),
                        PointState(150, 70),
                        PointState(200, 100),
                        PointState(200, 200),
                        PointState(100, 200),
                    ]
                ),
            ),
        )
        contour._state.style.rectangle_style.color.value = "white"
        contour._state.style.rectangle_style.outline_color.value = "black"
        contour._state.style.rectangle_style.outline_width.value = 2
        contour._state.style.line_style.width.value = 2

        contour.tag_bind(
            "<B1-Motion>",
            lambda ev, rectangle: rectangle._state.data.center.set(ev.x, ev.y),
            _type="rectangle",
        )
        contour.tag_bind(
            "<Button-3>",
            lambda _, rect: contour._state.data.remove(rect._state.data.center),
            _type="rectangle",
        )
        contour.tag_bind(
            "<Double-Button-1>",
            lambda event, line: contour._state.data.insert(
                contour._state.data.index(line._state.data.end),
                PointState(event.x, event.y),
            ),
            _type="line",
        )


if __name__ == "__main__":
    app = ContourApp()
    app.mainloop()
