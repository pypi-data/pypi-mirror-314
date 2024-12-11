import math

from hydreservoir.water_balance.v2.hydraulic_component.base_circular_culvert import BaseCircularCulvert


class CircularCulvertV2(BaseCircularCulvert):

    def calculate_circular_culvert_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        if water_level < self._elevation:
            return 0

        g = self._gravitational_acceleration
        e = self._discharge_coefficient
        jc = self._contraction_coefficient
        wc = self._radius
        a = opening
        r = wc

        theta = a / wc
        _A = r ** 2 * (theta - math.sin(theta)) / 2
        _H = water_level - self._elevation

        if _H <= 1.5 * a:
            return self._free_spillway.calculate_free_spillway_discharge(water_level, capacity)

        return jc * e * _A * math.sqrt(2 * g * _H)
