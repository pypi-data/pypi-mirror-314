from abc import ABC, abstractmethod

import numpy as np


class Adjustable(ABC):
    def __init__(
            self, opening: np.ndarray[float],
            discharge_coefficient: float
    ):
        self._opening = opening
        self._discharge_coefficient = discharge_coefficient



