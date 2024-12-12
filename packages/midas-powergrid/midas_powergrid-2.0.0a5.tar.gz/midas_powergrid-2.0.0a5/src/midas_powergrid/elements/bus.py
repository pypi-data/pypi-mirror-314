import logging
from typing import List

import pandapower as pp

from ..constraints.voltage_band import ConstraintVoltageBand
from .base import GridElement

LOG = logging.getLogger(__name__)


class PPBus(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "bus"

    @staticmethod
    def res_pp_key() -> str:
        return "res_bus"

    def __init__(self, index, grid, value):
        super().__init__(index, grid, LOG)

        self.in_service = True
        self.add_constraint(
            ConstraintVoltageBand(self, 1.0 - value, 1.0 + value)
        )
        self.load_indices: List[int] = []
        for idx, bus in zip(
            self.grid.get_value("load").index.values,
            self.grid.get_value("load", attr="bus").values,
        ):
            if bus == self.index:
                self.load_indices.append(int(idx))
        self.sgen_indices: List[int] = []
        for idx, bus in zip(
            self.grid.get_value("sgen").index.values,
            self.grid.get_value("sgen", attr="bus").values,
        ):
            if bus == self.index:
                self.sgen_indices.append(int(idx))

    def step(self, time):
        old_state = self.in_service
        self.in_service = True
        self.set_load_service_state(in_service=True)
        self.set_sgen_service_state(in_service=True)

        self._check(time)

        if old_state != self.in_service:
            if self.in_service:
                # Was off; but can switch on now?
                try:
                    self.grid.run_powerflow()
                    self._check(time)
                except pp.powerflow.LoadflowNotConverged:
                    self.set_load_service_state(in_service=False)
                    self.set_sgen_service_state(in_service=False)
                    self.in_service = False

        # Announce possible state changes
        if old_state != self.in_service:
            if not self.in_service:
                msg = (
                    f"At step {time}: Bus {self.index} out of service! "
                    f"(vm_pu: {self._constraints[0].violated_value}). "
                    f"Disabling loads {self.load_indices} and sgens "
                    f"{self.sgen_indices}"
                )
                LOG.debug(msg)
                try:
                    self.grid.run_powerflow()
                except pp.powerflow.LoadflowNotConverged:
                    LOG.debug("Bus disabled, LF still not converges.")
            else:
                LOG.debug(f"At step {time}: Bus {self.index} back in service!")
                try:
                    self.grid.run_powerflow()
                except pp.powerflow.LoadflowNotConverged:
                    LOG.debug("Bus re-enabled, LF not converging.")

        # We won't set the bus out of service; only the loads or sgens
        # connected to it
        # self.set_value("in_service", self.in_service)

        # Run powerflow so that the next unit does not automatically
        # switch off, too.

        return old_state != self.in_service

    def set_load_service_state(self, in_service: bool):
        for idx in self.load_indices:
            self.grid.set_value("load", idx, "in_service", in_service)

    def set_sgen_service_state(self, in_service: bool):
        for idx in self.sgen_indices:
            self.grid.set_value("sgen", idx, "in_service", in_service)
