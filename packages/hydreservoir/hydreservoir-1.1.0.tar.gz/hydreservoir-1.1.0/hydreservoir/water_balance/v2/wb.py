from typing import List, Union

import numpy as np
import pandas as pd

from hydreservoir.columns_constant import INFLOW, OUTFLOW, TIMESERIES, INTERVAL, DELTA, WATER_LEVEL, CAPACITY
from hydreservoir.water_balance.v2.hydraulic_component.core import Core


class WB:
    def __init__(
            self,
            timeseries: Union[np.ndarray[np.datetime64], np.datetime64],
            water_level: np.ndarray[float],
            capacity: np.ndarray[float],
    ):
        if not (len(timeseries) == len(water_level) == len(capacity)):
            raise ValueError("The lengths of 'timeseries', 'water_level', and 'capacity' must be the same.")

        self._components: List[Core] = []

        self._timeseries = timeseries
        self._water_level = water_level
        self._capacity = capacity

        self._interval = np.diff(timeseries, prepend=timeseries[0]).astype('timedelta64[s]').astype(int)
        self._delta = np.diff(capacity, prepend=capacity[0])

        self._size = len(timeseries)

    def add_component(self, component: Core):
        self._components.append(component)
        return self

    def remove_component(self, component: Core):
        self._components.remove(component)
        return self

    def get_components(self) -> List[Core]:
        return self._components

    def calculate(self):
        outflow = np.zeros(self._size)

        data_dict = {
            TIMESERIES: self._timeseries,
            WATER_LEVEL: self._water_level,
            CAPACITY: self._capacity,
            DELTA: self._delta,
            INTERVAL: self._interval
        }

        for component in self._components:
            c_outflow = component.provide_discharge(self._water_level, self._capacity)
            if len(c_outflow) != self._size:
                raise ValueError(
                    f"Invalid outflow size for component '{component.name}': "
                    f"received {len(c_outflow)}, but expected {self._size}."
                )
            data_dict[f'{type(component).__name__}.{component.name}.{component.id}'] = c_outflow
            outflow += c_outflow

        inflow = ((outflow * self._interval) + self._delta * 10 ** 6) / self._interval
        inflow[0] = 0
        inflow[inflow < 0] = 0

        data_dict[INFLOW] = inflow
        data_dict[OUTFLOW] = outflow

        return pd.DataFrame(data_dict)
