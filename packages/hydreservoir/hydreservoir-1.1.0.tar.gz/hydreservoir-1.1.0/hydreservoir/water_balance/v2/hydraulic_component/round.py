from abc import ABC, abstractmethod


class Round(ABC):
    def __init__(self, radius: float):
        self._radius = radius
