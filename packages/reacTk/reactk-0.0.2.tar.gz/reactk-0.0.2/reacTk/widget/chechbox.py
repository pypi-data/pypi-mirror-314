import tkinter as tk
from tkinter import ttk
from typing import Optional

from widget_state import BoolState, DictState, HigherOrderState, StringState

from ..decorator import stateful
from ..state import to_tk_var


class CheckBoxProperties(DictState):

    def __init__(
        self,
        label: Optional[StringState] = None,
    ):
        super().__init__()

        self.label = label if label is not None else StringState(None)


CheckBoxData = BoolState


class CheckBoxState(HigherOrderState):

    def __init__(self, data: CheckBoxData, props: Optional[CheckBoxProperties] = None):
        super().__init__()

        self.data = data
        self.props = props if props is not None else CheckBoxProperties()


@stateful
class Checkbox(ttk.Checkbutton):

    def __init__(self, parent: tk.Widget, state: CheckBoxState):
        super().__init__(parent, variable=to_tk_var(state.data))

    def draw(self, state):
        self.config(
            text=state.props.label.value,
        )


__all__ = [
    Checkbox,
    CheckBoxData,
    CheckBoxProperties,
    CheckBoxState,
]
