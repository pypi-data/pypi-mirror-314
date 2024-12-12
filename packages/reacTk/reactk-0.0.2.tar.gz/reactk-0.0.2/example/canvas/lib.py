"""
Bundle common functionalities of all examples."
"""

import tkinter as tk


class App(tk.Tk):

    def __init__(self, width: int = 512, height: int = 512) -> None:
        super().__init__()
        self.geometry("1600x900")
        self.bind("<Key-q>", lambda event: exit(0))

        # self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def init_widgets(self) -> None:
        pass
