from abc import ABC, abstractmethod

import numpy as np

from hydreservoir.water_balance.v2.hydraulic_component.base_spillway import BaseSpillway
from hydreservoir.water_balance.v2.hydraulic_component.straight import Straight


class BaseFreeSpillway(BaseSpillway, Straight, ABC):
    def __init__(
            self, name: str, elevation: float,
            dimension: float,
            spillway_discharge_coefficient: float = 0.36,
            gravitational_acceleration: float = 9.81,
    ):
        BaseSpillway.__init__(self, name, elevation, spillway_discharge_coefficient, gravitational_acceleration)
        Straight.__init__(self, dimension)

    @abstractmethod
    def calculate_free_spillway_discharge(self, water_level: float, capacity: float) -> float:
        raise NotImplementedError

    def provide_discharge(self, water_level: np.ndarray[float], capacity: np.ndarray[float]) -> np.ndarray[float]:
        return np.vectorize(self.calculate_free_spillway_discharge)(water_level, capacity)
