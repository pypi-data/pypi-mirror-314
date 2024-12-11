import tkinter as tk
from typing import Optional

from widget_state import BoolState, DictState, HigherOrderState, IntState, StringState

from ..decorator import stateful


def to_tk(bool_state: BoolState) -> tk.BooleanVar:
    bool_var = tk.BooleanVar(value=bool_state.value)

    bool_state.on_change(lambda _: bool_var.set(bool_state.value))
    bool_var.trace_add("write", lambda *_: bool_state.set(bool_var.get()))

    return bool_var


class CheckBoxStyle(DictState):

    def __init__(
        self,
        label: Optional[StringState] = None,
        background_color: Optional[StringState] = None,
        highlight_thickness: Optional[IntState] = None,
    ):
        super().__init__()

        self.label = label if label is not None else StringState(None)
        self.background_color = (
            background_color if background_color is not None else StringState(None)
        )
        self.highlight_thickness = (
            highlight_thickness if highlight_thickness is not None else IntState(None)
        )


CheckBoxData = BoolState


class CheckboxState(HigherOrderState):

    def __init__(self, data: CheckBoxData, style: Optional[CheckBoxStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else CheckBoxStyle()


@stateful
class Checkbox(tk.Checkbutton):

    def __init__(self, parent: tk.Widget, state: CheckboxState):
        super().__init__(parent, variable=to_tk(state.data))

    def draw(self, state):
        self.config(
            text=state.style.label.value,
            background=state.style.background_color.value,
            highlightthickness=state.style.highlight_thickness.value,
        )
