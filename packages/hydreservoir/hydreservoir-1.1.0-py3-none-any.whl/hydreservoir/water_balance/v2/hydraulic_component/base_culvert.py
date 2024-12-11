from abc import ABC

from hydreservoir.water_balance.v2.hydraulic_component.passive import Passive


class BaseCulvert(Passive, ABC):
    def __init__(
            self, name: str, elevation: float, gravitational_acceleration: float,
            contraction_coefficient: float
    ):
        super().__init__(name, elevation, gravitational_acceleration)

        self._contraction_coefficient = contraction_coefficient
