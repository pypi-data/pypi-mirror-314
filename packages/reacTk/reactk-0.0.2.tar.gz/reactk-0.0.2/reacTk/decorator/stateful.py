import functools
from uuid import uuid4 as uuid
from typing import ParamSpec, Type, TypeVar

import tkinter as tk
from widget_state import State

T = TypeVar("T")
P = ParamSpec("P")


def stateful(cls: Type[T]) -> Type[T]:
    """
    Make a widget stateful.

    This means that it has a state attribute and if its
    state changes, its `draw` method is called so
    that its appearance changes.

    There are three conditions:
      * the widget must either extend from the tk.Widget class or
        return a tk.Widget via its `widget` attribute
      * the widget must receive a `State` as positional or keyword argument
      * the widget must implement a `draw` method

    Note: This functions maps a change of the `state` to a virtual
    tkinter event. The reason for this is that state changes may
    occur in separate threads. Firing a tkinter event means that the
    GUI thread is responsible for executing the `draw` function.
    """
    orig_init = cls.__init__

    @functools.wraps(orig_init)
    def __init__(self: T, *args: P.args, **kwargs: P.kwargs) -> None:
        if "state" in kwargs and isinstance(kwargs["state"], State):
            state = kwargs["state"]
        else:
            for arg in args:
                if isinstance(arg, State):
                    state = arg
                    break
        assert state is not None, f"Could not detect state in {args=} or {kwargs=}"

        self.__dict__["_state"] = state
        self.__dict__["event_id"] = (
            f"<<{str(uuid())}_{self._state.__class__.__name__}>>"
        )

        orig_init(self, *args, **kwargs)

        assert isinstance(self, tk.Widget) or (
            hasattr(self, "widget") and isinstance(self.widget, tk.Widget)
        ), f"Widget {cls.__name__} is not a tk.Widget nor does it provide access to one via a `widget` attribute"
        assert hasattr(
            self, "draw"
        ), f"Widget {cls.__name__} doe not provide a `draw` function"

        widget = self if isinstance(self, tk.Widget) else self.widget

        """
        The next part is a little complicated.
        We first register the draw method to directly react to state changes (and trigger it immediately).
        Afterwards we use tkinters `after` method to remove this callback and instead fire an event, which we
        bind the widget to.
        The reason for this convoluted event handling is that using tk events is only possible
        once the mainloop has started. Thus, if we do not do it this way, changes done to the state before
        the mainloop will not be handled.
        """
        callback_id = self._state.on_change(self.draw, trigger=True)

        def after_mainloop():
            self._state.remove_callback(callback_id)
            self._state.on_change(lambda _: widget.event_generate(self.event_id))
            widget.bind(self.event_id, lambda _: self.draw(self._state))

        widget.after(0, after_mainloop)

    cls.__init__ = __init__
    return cls
