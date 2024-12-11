from dataclasses import dataclass
import functools
import threading
import time
from typing import Callable, Generic, Optional, TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


@dataclass
class RecurrencyData(Generic[P]):
    def __init__(self, interval: float) -> None:
        self.interval = interval
        self.lock = threading.Lock()
        self.pending_call: Optional[threading.Thread] = None

        self.last_call = 0.0
        self.last_args: Optional[P.args] = None
        self.last_kwargs: Optional[P.kwargs] = None


def _recurrency_filter(func: Callable[P, None], interval: float) -> Callable[P, None]:
    recurrency_data = RecurrencyData[P](interval=interval)

    def trigger_pending() -> None:
        # print("Trigger pending")
        with recurrency_data.lock:
            recurrency_data.last_call = time.time()
            recurrency_data.pending_call = None
        assert recurrency_data.last_args is not None
        assert recurrency_data.last_kwargs is not None
        func(*recurrency_data.last_args, **recurrency_data.last_kwargs)

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        with recurrency_data.lock:
            current_time = time.time()
            passed_time = current_time - recurrency_data.last_call
            if passed_time >= recurrency_data.interval:
                recurrency_data.last_call = current_time
                func(*args, **kwargs)
            else:
                # print("Schedule")
                recurrency_data.last_args = args
                # print(recurrency_data)
                recurrency_data.last_kwargs = kwargs
                # print(recurrency_data)
                if recurrency_data.pending_call is None:
                    # print(f"Create pending")
                    remaining_time = recurrency_data.interval - passed_time
                    recurrency_data.pending_call = threading.Timer(
                        remaining_time, trigger_pending
                    )
                    recurrency_data.pending_call.start()

    return wrapper


def recurrency_filter(interval: float) -> functools.partial[Callable[P, None]]:
    return functools.partial(_recurrency_filter, interval=interval)
