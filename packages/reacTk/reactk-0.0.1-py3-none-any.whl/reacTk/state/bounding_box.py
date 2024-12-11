from widget_state import DictState, IntState

from .point import PointState


class BoundingBoxState(DictState):

    def __init__(
        self,
        x1: int | IntState,
        y1: int | IntState,
        x2: int | IntState,
        y2: int | IntState,
    ):
        super().__init__()

        self.x1 = IntState(x1) if isinstance(x1, int) else x1
        self.y1 = IntState(y1) if isinstance(y1, int) else y1
        self.x2 = IntState(x2) if isinstance(x2, int) else x2
        self.y2 = IntState(y2) if isinstance(y2, int) else y2

    def tlbr(self) -> tuple[int, int, int, int]:
        return (self.x1.value, self.y1.value, self.x2.value, self.y2.value)

    def top_left(self):
        return PointState(self.x1, self.y1)

    def top_right(self):
        return PointState(self.x2, self.y1)

    def bottom_left(self):
        return PointState(self.x1, self.y2)

    def bottom_right(self):
        return PointState(self.x2, self.y2)
