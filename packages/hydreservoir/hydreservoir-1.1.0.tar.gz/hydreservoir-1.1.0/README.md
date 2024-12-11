# HydReservoir

[![PyPI Version](https://img.shields.io/pypi/v/hydreservoir)](https://pypi.org/project/hydreservoir/)
[![Python Compatibility](https://img.shields.io/pypi/pyversions/hydreservoir)](https://pypi.org/project/hydreservoir/)
[![License](https://img.shields.io/github/license/duynguyen02/hydreservoir)](https://github.com/duynguyen02/hydreservoir)

## Overview

`HydReservoir` is a comprehensive Python library for advanced hydrological calculations and water reservoir management.

## Key Features

- Detailed water balance calculations
- Complex hydraulic system modeling
- Support for multiple hydraulic components:
    - Pumps
    - Box culverts
    - Circular culverts
    - Gated spillways
    - Free spillways
    - Unknown discharge sources
- Advanced reservoir regulation utilities

## Installation

Install HydReservoir quickly using pip:

```bash
pip install hydreservoir
```

## Getting Started

### 1. Water Balance Calculation

```python
import pandas as pd

from hydreservoir.water_balance.v2.hydraulic_component import BoxCulvert
from hydreservoir.water_balance.v2.hydraulic_component import CircularCulvert
from hydreservoir.water_balance.v2.hydraulic_component import CircularCulvertV2
from hydreservoir.water_balance.v2.hydraulic_component import FreeSpillway
from hydreservoir.water_balance.v2.hydraulic_component import Pump
from hydreservoir.water_balance.v2.hydraulic_component import Unknown
from hydreservoir.water_balance.v2.hydraulic_component import GatedSpillway
from hydreservoir.water_balance.v2.wb import WB

df = pd.read_csv('data.csv')

free_spillway = FreeSpillway(
    'FS1', 109.3, 19.0
)

gated_spillway = GatedSpillway(
    'GS1', 109.3, 19.0,
    df['GatedA'].to_numpy(), free_spillway
)

circular_culvert = CircularCulvert(
    'CC1', 102.5, 0.4, df['CircularA'].to_numpy(), free_spillway,
    discharge_coefficient=0.9, contraction_coefficient=1.0
)

circular_culvert_v2 = CircularCulvertV2(
    'CC2', 102.5, 0.4, df['CircularA'].to_numpy(), free_spillway,
    discharge_coefficient=0.9, contraction_coefficient=1.0
)

box_culvert = BoxCulvert(
    'BC1', 102.5, 0.4, df['BoxA'].to_numpy(), free_spillway
)

pump = Pump(
    'P1', df['P'].to_numpy()
)

unknown = Unknown(
    'U1', df['P'].to_numpy()
)

timeseries = pd.to_datetime(df['Timeseries'])

wb = WB(
    timeseries.to_numpy(),
    df['WaterLevel'].astype(float).to_numpy(),
    df['Capacity'].astype(float).to_numpy(),
)

(wb.add_component(circular_culvert_v2).add_component(free_spillway)
 .add_component(pump).add_component(box_culvert))

wb.calculate().to_csv('result.csv', index=False)
```

### Result DataFrame Columns

The water balance calculation returns a detailed DataFrame with the following columns:

| Column Name                                      | Description                                                          | Unit                           | Example      |
|--------------------------------------------------|----------------------------------------------------------------------|--------------------------------|--------------|
| `Timeseries`                                     | Timestamp for the measurement                                        | Datetime                       | `2022-01-01` |
| `WaterLevel`                                     | Current water level in the reservoir                                 | Meters (m)                     | `109.3`      |
| `Capacity`                                       | Reservoir capacity corresponding to the current water level          | Cubic meters (10^6m³)          | `2.53`       |
| `Delta`                                          | Change in water level since the previous measurement                 | Meters (m)                     | `0.0`        |
| `Interval`                                       | Time interval between consecutive measurements                       | Seconds                        | `86400`      |
| `FreeSpillway.<Free Spillway ID>.<uuid>`         | Flow rate through the free spillway with the specified ID            | Cubic meters per second (m³/s) | `0.0`        |
| `GatedSpillway.<Gated Spillway ID>.<uuid>`       | Flow rate through a gated spillway port with the specified ID        | Cubic meters per second (m³/s) | `0.0`        |
| `CircularCulvert.<Circular Culvert ID>.<uuid>`   | Flow rate through the circular culvert with the specified ID         | Cubic meters per second (m³/s) | `4.046643`   |
| `CircularCulvertV2.<Circular Culvert ID>.<uuid>` | Flow rate through the updated circular culvert with the specified ID | Cubic meters per second (m³/s) | `0.131839`   |
| `BoxCulvert.<Box Culvert ID>.<uuid>`             | Flow rate through the box culvert with the specified ID              | Cubic meters per second (m³/s) | `0.573937`   |
| `Pump.<Pump ID>.<uuid>`                          | Discharge rate for the pump with the specified ID                    | Cubic meters per second (m³/s) | `0.0`        |
| `Unknown.<Unknown Source ID>.<uuid>`             | Discharge rate for an unknown source with the specified ID           | Cubic meters per second (m³/s) | `0.0`        |
| `Inflow`                                         | Total inflow into the reservoir                                      | Cubic meters per second (m³/s) | `4.75242`    |
| `Outflow`                                        | Total outflow from all components                                    | Cubic meters per second (m³/s) | `4.75242`    |

### 2. Custom Hydraulic Components

```python
import numpy as np

from hydreservoir.water_balance.v2.hydraulic_component import BaseFreeSpillway, BaseGatedSpillway, BaseCircularCulvert,\
    BaseBoxCulvert, SimpleDischarge
from hydreservoir.water_balance.v2.hydraulic_component.core import Core


class CustomFromScratch(Core):

    def provide_discharge(self, water_level: np.ndarray[float], capacity: np.ndarray[float]) -> np.ndarray[float]:
        return np.zeros(len(water_level))


class CustomFreeSpillway(BaseFreeSpillway):
    def calculate_free_spillway_discharge(self, water_level: float, capacity: float) -> float:
        m = self._spillway_discharge_coefficient
        g = self._gravitational_acceleration
        _B = self._dimension
        _H = water_level - self._elevation
        # do something ...
        return 0


class CustomGatedSpillway(BaseGatedSpillway):
    def calculate_gated_spillway_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        # access properties
        # do something ...
        return 0


class CustomCircularCulvert(BaseCircularCulvert):
    def calculate_circular_culvert_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        # access properties
        # do something ...
        return 0


class CustomBoxCulvert(BaseBoxCulvert):
    def calculate_box_culvert_discharge(self, water_level: float, capacity: float, opening: float) -> float:
        # access properties
        # do something ...
        return 0


class CustomPump(SimpleDischarge):
    def provide_discharge(
            self, water_level: np.ndarray[float], capacity: np.ndarray[float]
    ) -> np.ndarray[float]:
        return self._discharge

```

### 3. Reservoir Regulation Analysis

```python
from hydreservoir.regulation import regulation
from hydreservoir.regulation.dataset import Dataset as RDataset

# ... calculate init components for water balance
df = wb.calculate().to_csv('result.csv', index=False)

# Regulation analysis
P = 90.0
eps = 0.1
P_n = regulation.P_n(RDataset.from_wb_df_to_dataset(df), V_c=1.0, gt_10_years=True)

print(P_n - P <= eps)
```

### 3. Mapping Functions for Water Levels and Capacities

These functions allow efficient mapping between water levels and reservoir capacities, with optional support for nearest
neighbor interpolation.

`get_capacity`
Maps a single water level to its corresponding capacity using a provided mapping dictionary. Supports optional nearest
neighbor interpolation for unmatched values.

```python
from hydreservoir.utils import get_capacity

water_level_capacity_map = {0.0: 0.0, 1.0: 100.0, 2.0: 200.0}
capacity = get_capacity(1.5, water_level_capacity_map, nearest_mapping=True)
print(capacity)  # Output: 100.0
```

`map_capacity`
Maps an array of water levels to their corresponding capacities using a provided mapping dictionary. Supports optional
nearest neighbor interpolation for unmatched values.

```python
from hydreservoir.utils import map_capacity

water_level_capacity_map = {0.0: 0.0, 1.0: 100.0, 2.0: 200.0}
water_levels = [0.5, 1.5, 2.0]
capacities = map_capacity(water_levels, water_level_capacity_map, nearest_mapping=True)
print(capacities)  # Output: [0.0, 100.0, 200.0]
```

`get_water_level`
Maps a single capacity to its corresponding water level using a provided mapping dictionary. Supports optional nearest
neighbor interpolation for unmatched values.

```python
from hydreservoir.utils import get_water_level

capacity_water_level_map = {0.0: 0.0, 100.0: 1.0, 200.0: 2.0}
water_level = get_water_level(150.0, capacity_water_level_map, nearest_mapping=True)
print(water_level)  # Output: 1.0
```

`map_water_level`
Maps an array of capacities to their corresponding water levels using a provided mapping dictionary. Supports optional
nearest neighbor interpolation for unmatched values.

```python
from hydreservoir.utils import map_water_level

capacity_water_level_map = {0.0: 0.0, 100.0: 1.0, 200.0: 2.0}
capacities = [50.0, 150.0, 200.0]
water_levels = map_water_level(capacities, capacity_water_level_map, nearest_mapping=True)
print(water_levels)  # Output: [0.0, 1.0, 2.0]
```

## License

This library is released under the MIT License.