from abc import ABC

from hydreservoir.water_balance.v2.hydraulic_component.base_free_spillway import BaseFreeSpillway


class NeedFreeSpillway(ABC):
    def __init__(
            self,
            free_spillway: BaseFreeSpillway,
    ):
        self._free_spillway = free_spillway
