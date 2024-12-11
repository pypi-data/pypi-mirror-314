"""
Bundle common functionalities of all examples."
"""

import tkinter as tk


class App(tk.Tk):

    def __init__(self, width: int = 512, height: int = 512) -> None:
        super().__init__()
        self.bind("<Key-q>", lambda event: exit(0))

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid()

    def init_widgets(self) -> None:
        pass
