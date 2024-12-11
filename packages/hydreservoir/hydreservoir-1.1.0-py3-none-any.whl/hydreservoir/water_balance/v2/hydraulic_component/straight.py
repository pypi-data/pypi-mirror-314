from abc import ABC


class Straight(ABC):
    def __init__(
            self, dimension: float
    ):
        self._dimension = dimension
