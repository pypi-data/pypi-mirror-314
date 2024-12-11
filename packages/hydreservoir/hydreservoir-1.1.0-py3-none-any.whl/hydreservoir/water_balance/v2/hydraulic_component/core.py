from abc import ABC, abstractmethod
import uuid

import numpy as np


class Core(ABC):

    def __init__(self, name: str):
        self._id = uuid.uuid4()
        self._name = name

    @abstractmethod
    def provide_discharge(
            self, water_level: np.ndarray[float], capacity: np.ndarray[float],
    ) -> np.ndarray[float]:
        raise NotImplementedError

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
