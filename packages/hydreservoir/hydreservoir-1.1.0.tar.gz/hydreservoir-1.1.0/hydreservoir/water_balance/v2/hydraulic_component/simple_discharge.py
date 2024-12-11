import numpy as np
from hydreservoir.water_balance.v2.hydraulic_component.core import (
    Core,
)


class SimpleDischarge(Core):
    def __init__(self, name, discharge: np.ndarray[float]):
        super().__init__(name)

        self._discharge = discharge

    def provide_discharge(
            self, water_level: np.ndarray[float], capacity: np.ndarray[float]
    ) -> np.ndarray[float]:
        return self._discharge
