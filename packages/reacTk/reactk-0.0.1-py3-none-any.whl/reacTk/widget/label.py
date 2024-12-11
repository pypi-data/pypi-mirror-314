import tkinter as tk
from typing import Optional

from widget_state import DictState, HigherOrderState, StringState

from ..decorator import stateful

LabelData = StringState


class LabelStyle(DictState):

    def __init__(self, background_color: Optional[StringState] = None):
        super().__init__()

        self.background_color = (
            background_color if background_color is not None else StringState(None)
        )


class LabelState(HigherOrderState):

    def __init__(self, data: LabelData, style: Optional[LabelStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else LabelStyle()


@stateful
class Label(tk.Label):

    def __init__(self, parent: tk.Widget, state: LabelState):
        super().__init__(parent)

    def draw(self, state: LabelState) -> None:
        self.config(
            text=state.data.value, background=state.style.background_color.value
        )
