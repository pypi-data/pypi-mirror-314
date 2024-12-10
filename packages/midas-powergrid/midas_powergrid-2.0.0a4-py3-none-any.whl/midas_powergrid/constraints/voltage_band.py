import numpy as np

from ..elements.base import GridElement
from .base import Constraint


class ConstraintVoltageBand(Constraint):
    def __init__(
        self, element: GridElement, lower_band: float, upper_band: float
    ):
        super().__init__(element)

        self._vm_pu_max = upper_band
        self._vm_pu_min = lower_band

        self.over_voltage = False
        self.under_voltage = False

    def check(self, time) -> bool:
        self._satisfied = True
        voltage = self._element.grid.get_value(
            "res_bus", self._element.index, "vm_pu"
        )

        self.over_voltage = voltage > self._vm_pu_max
        self.under_voltage = voltage < self._vm_pu_min

        if np.isnan(voltage) or self.over_voltage or self.under_voltage:
            self._satisfied = False
            self.violated_value = voltage

        return self._satisfied

    def handle_violation(self):
        self._element.set_load_service_state(in_service=False)
        self._element.set_sgen_service_state(in_service=False)

        self._element.in_service = False
