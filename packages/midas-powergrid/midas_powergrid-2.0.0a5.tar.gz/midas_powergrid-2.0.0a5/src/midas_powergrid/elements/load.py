import logging

import pandapower as pp

from ..constraints.load_voltage_change import ConstraintLoadVoltageChange
from .base import GridElement

LOG = logging.getLogger(__name__)


class PPLoad(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "load"

    @staticmethod
    def res_pp_key() -> str:
        return "res_load"

    def __init__(self, index, grid, value=0.02):
        super().__init__(index, grid, LOG)

        self.current_bus_voltage = 1.0
        self.in_service = True
        self.p_mw = grid.get_value(self.pp_key(), index, "p_mw")
        self.q_mvar = grid.get_value(self.pp_key(), index, "q_mvar")

        self._constraints.append(ConstraintLoadVoltageChange(self, value))

    def step(self, time):
        old_state = self.in_service
        self.in_service = True
        self._check(time)

        self.set_value("p_mw", self.p_mw)
        self.set_value("q_mvar", self.q_mvar)
        self.set_value("in_service", self.in_service)

        # Run powerflow so that the next unit does not automatically
        # switch off, too.
        if old_state != self.in_service:
            if not self.in_service:
                LOG.debug(
                    f"At step {time}: Load {self.index} with p={self.p_mw:.5f}"
                    f" and q={self.q_mvar:.5f} out of service (Bus voltage: "
                    f"{self.current_bus_voltage:.5f})"
                )
                try:
                    self.grid.run_powerflow()
                except pp.LoadflowNotConverged:
                    LOG.debug("Line disabled. PF still not converging.")
            else:
                LOG.debug(
                    f"At step {time}: Load {self.index} back in service."
                )
                try:
                    self.grid.run_powerflow()
                except pp.LoadflowNotConverged:
                    LOG.debug("Load re-enabled. PF not converging.")

        return old_state != self.in_service
