from abc import ABC, abstractmethod

import numpy as np

from hydreservoir.water_balance.v2.hydraulic_component.adjustable import Adjustable
from hydreservoir.water_balance.v2.hydraulic_component.base_free_spillway import BaseFreeSpillway
from hydreservoir.water_balance.v2.hydraulic_component.base_culvert import BaseCulvert
from hydreservoir.water_balance.v2.hydraulic_component.need_free_spillway import NeedFreeSpillway
from hydreservoir.water_balance.v2.hydraulic_component.straight import Straight


class BaseBoxCulvert(BaseCulvert, Straight, Adjustable, NeedFreeSpillway, ABC):
    def __init__(
            self,
            name: str, elevation: float,
            dimension: float,
            opening: np.ndarray[float],
            free_spillway: BaseFreeSpillway,
            contraction_coefficient: float = 0.94,
            discharge_coefficient: float = 0.63,
            gravitational_acceleration: float = 9.81,
    ):
        BaseCulvert.__init__(self, name, elevation, gravitational_acceleration, contraction_coefficient)
        Straight.__init__(self, dimension)
        Adjustable.__init__(self, opening, discharge_coefficient)
        NeedFreeSpillway.__init__(self, free_spillway)

    @abstractmethod
    def calculate_box_culvert_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        raise NotImplementedError

    def provide_discharge(self, water_level: np.ndarray[float], capacity: np.ndarray[float]) -> np.ndarray[float]:
        return np.vectorize(self.calculate_box_culvert_discharge)(water_level, capacity, self._opening)
