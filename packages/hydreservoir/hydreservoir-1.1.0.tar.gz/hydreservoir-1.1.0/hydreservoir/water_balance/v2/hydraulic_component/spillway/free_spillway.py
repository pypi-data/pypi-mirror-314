import math

from hydreservoir.water_balance.v2.hydraulic_component.base_free_spillway import BaseFreeSpillway


class FreeSpillway(BaseFreeSpillway):
    def calculate_free_spillway_discharge(self, water_level: float, capacity: float) -> float:
        if water_level < self._elevation:
            return 0

        m = self._spillway_discharge_coefficient
        g = self._gravitational_acceleration
        _B = self._dimension
        _H = water_level - self._elevation

        return m * _B * math.sqrt(2 * g) * (_H ** (3 / 2))
