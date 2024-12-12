import tkinter as tk
from tkinter import ttk

from reacTk.widget.chechbox import (
    Checkbox,
    CheckBoxData,
    CheckBoxState,
    CheckBoxProperties,
)
from reacTk.widget.label import Label, LabelState


root = tk.Tk()
root.bind("<Key-q>", lambda event: exit(0))
root.update_idletasks()
print(root.winfo_geometry())

frame = ttk.Frame(root)
frame.grid()

style = ttk.Style()
style.theme_use("clam")

checkbox = Checkbox(
    frame,
    CheckBoxState(
        CheckBoxData(False),
        CheckBoxProperties(label="Disabled"),
    ),
)
checkbox._state.data.on_change(
    lambda data: checkbox._state.props.label.set(
        "Enabled" if data.value else "Disabled"
    )
)
# checkbox._state.data.on_change(
#     lambda data: style.configure(
#         "TCheckbutton", background="red" if data.value else "green"
#     ),
# )
checkbox.grid(row=0, column=0, padx=50, pady=50)

label = Label(frame, LabelState("Hello World"))
label.grid(row=1, column=0, padx=50, pady=50)

root.mainloop()
