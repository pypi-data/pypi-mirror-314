import math

from hydreservoir.water_balance.v2.hydraulic_component.base_gated_spillway import BaseGatedSpillway


class GatedSpillway(BaseGatedSpillway):

    def calculate_gated_spillway_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        if water_level < self._elevation:
            return 0

        e = self._discharge_coefficient
        m = self._spillway_discharge_coefficient
        g = self._gravitational_acceleration
        _B = self._dimension
        a = opening

        _H = water_level - self._elevation

        if _H <= 1.5 * a:
            return self._free_spillway.calculate_free_spillway_discharge(water_level, capacity)

        return e * m * _B * a * math.sqrt(2 * g * (_H - e * a))
