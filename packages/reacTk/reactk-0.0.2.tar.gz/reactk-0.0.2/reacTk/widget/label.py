import tkinter as tk
from tkinter import ttk

from widget_state import StringState

from ..decorator import stateful

LabelState = StringState


@stateful
class Label(ttk.Label):

    def __init__(self, parent: tk.Widget, state: LabelState):
        super().__init__(parent)

    def draw(self, state: LabelState) -> None:
        self.config(text=state.value)
