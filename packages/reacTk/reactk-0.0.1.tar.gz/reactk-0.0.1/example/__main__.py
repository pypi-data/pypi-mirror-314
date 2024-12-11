import tkinter as tk

from reacTk.widget.chechbox import Checkbox, CheckBoxData, CheckboxState, CheckBoxStyle
from reacTk.widget.label import Label, LabelData, LabelState

root = tk.Tk()
root.bind("<Key-q>", lambda event: exit(0))

checkbox = Checkbox(
    root,
    CheckboxState(
        CheckBoxData(False),
        CheckBoxStyle(label="Disabled", background_color="red", highlight_thickness=0),
    ),
)
checkbox._state.data.on_change(
    lambda data: checkbox._state.style.background_color.set(
        "green" if data.value else "red"
    )
)
checkbox.grid(row=0, column=0, padx=50, pady=50)

label = Label(root, LabelState(LabelData("Label")))
label._state.style.background_color.set("#757575")
label.grid(row=1, column=0, padx=50, pady=50)

root.mainloop()
