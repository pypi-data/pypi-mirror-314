import math

from hydreservoir.water_balance.v2.hydraulic_component.base_box_culvert import BaseBoxCulvert


class BoxCulvert(BaseBoxCulvert):

    def calculate_box_culvert_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        if water_level < self._elevation:
            return 0

        _H = water_level - self._elevation
        e = self._discharge_coefficient
        jc = self._contraction_coefficient
        g = self._gravitational_acceleration
        a = opening
        _B = self._dimension

        if _H <= 1.5 * a:
            return self._free_spillway.calculate_free_spillway_discharge(water_level, capacity)

        return e * jc * _B * a * math.sqrt(2 * g * (_H - e * a))
