from dataclasses import dataclass
import functools
import threading
from typing import Callable, Generic, Optional, ParamSpec


P = ParamSpec("P")


@dataclass
class AsyncData(Generic[P]):
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.current_call: Optional[threading.Thread] = None
        self.pending_call: Optional[threading.Thread] = None

        self.last_args: Optional[P.args] = None
        self.last_kwargs: Optional[P.kwargs] = None


def asynchron(func: Callable[P, None]) -> Callable[P, None]:
    async_data = AsyncData()

    def trigger_pending() -> None:
        async_data.current_call.join()

        with async_data.lock:
            async_data.pending_call = None

            async_data.current_call = threading.Thread(
                target=func, args=async_data.last_args, kwargs=async_data.last_kwargs
            )
            async_data.current_call.start()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        with async_data.lock:
            if async_data.current_call is None:
                async_data.current_call = threading.Thread(
                    target=func, args=args, kwargs=kwargs
                )
                async_data.current_call.start()
                return

            async_data.last_args = args
            async_data.last_kwargs = kwargs
            if (
                async_data.pending_call is None
                or async_data.pending_call.is_alive() is False
            ):
                async_data.pending_call = threading.Thread(target=trigger_pending)
                async_data.pending_call.start()

    return wrapper
