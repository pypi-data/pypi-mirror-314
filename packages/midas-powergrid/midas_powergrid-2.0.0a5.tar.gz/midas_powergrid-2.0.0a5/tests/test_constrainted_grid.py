import unittest

from midas_powergrid.model.static import PandapowerGrid


class TestConstraintedGrid(unittest.TestCase):
    def test_line_constraints(self):
        gparams = {
            "constant_load_p_mw": 0.7,  # 0.5
            "constant_load_q_mvar": 0.23,  # 0.17
            "constant_sgen_p_mw": 0.4,  # 0.3
            "constant_sgen_q_mvar": -0.13,  # -0.1
            "constraints": [["line", 100]],
            "gridfile": "midasmv",
        }
        self.grid = PandapowerGrid(gparams)

        step_size = 60
        results = []
        setpoints = []
        for i in range(100):
            setpoints.append(0.7 + i * 0.05)
            self.grid.set_inputs("load", 1, {"p_mw": setpoints[-1]})
            # print(self.grid.grid.load.iloc[1]["p_mw"])
            self.grid.run_powerflow(i * step_size)
            results.append(self.grid.get_outputs())

        checks = []
        for i, res in enumerate(results):
            checks.append(
                self._assert_line_loading_below_limit(res, 100, setpoints[i])
            )
        # print(checks)

    def _assert_line_loading_below_limit(self, results, limit, p_set):
        lines = {k: v for k, v in results.items() if "line" in k}
        loadings = {
            line: val
            for line, data in lines.items()
            for key, val in data.items()
            if "loading" in key
        }
        checks = {}
        for line, loading in loadings.items():
            checks[line] = loading <= limit

            self.assertLessEqual(
                loading,
                limit,
                msg=f"Loading of line {line} is above limit: {loading} "
                f"/ {limit}",
            )

        # print(loadings)
        return checks

    @unittest.skip
    def test_line_disables_after_violation(self):
        self.grid = PandapowerGrid()
        gparams = {
            "constant_load_p_mw": 0.7,  # 0.5
            "constant_load_q_mvar": 0.23,  # 0.17
            "constant_sgen_p_mw": 0.4,  # 0.3
            "constant_sgen_q_mvar": -0.13,  # -0.1
            "constraints": [["line", 100]],
        }
        self.grid.setup("midasmv", 0, gparams)
        self.grid.set_inputs("load", 1, {"p_mw": 1.5})
        self.grid.run_powerflow(0)
        # results = self.grid.get_outputs()
        # print()

    def test_voltage_constraints(self):
        gparams = {
            "constant_load_p_mw": 0.7,  # 0.5
            "constant_load_q_mvar": 0.23,  # 0.17
            "constant_sgen_p_mw": 0.4,  # 0.3
            "constant_sgen_q_mvar": -0.13,  # -0.1
            "gridfile": "midasmv",
        }
        self.ugrid = PandapowerGrid(gparams)

        gparams["constraints"] = [["sgen", 0.05], ["load", 0.02], ["bus", 0.1]]
        self.grid = PandapowerGrid(gparams)
        step_size = 60

        results = []
        uresults = []
        setpoints = []
        for i in range(100):
            setpoints.append(0.7 + i * 0.05)
            self.grid.set_inputs("load", 1, {"p_mw": setpoints[-1]})
            self.grid.run_powerflow(i * step_size)
            results.append(self.grid.get_outputs())

            self.ugrid.set_inputs("load", 1, {"p_mw": setpoints[-1]})
            self.ugrid.run_powerflow(i * step_size)
            uresults.append(self.ugrid.get_outputs())

        checks = []
        for i, (ures, res) in enumerate(zip(uresults, results)):
            checks.append(
                self._assert_voltage_within_limits(
                    ures, res, 0.9, 1.1, setpoints[i]
                )
            )
        # print(checks)

    def _assert_voltage_within_limits(
        self, uresults, results, low, high, p_set
    ):
        ubuses = {k: v for k, v in uresults.items() if "bus" in k}
        uvm_pus = {
            bus: val
            for bus, data in ubuses.items()
            for key, val in data.items()
            if "vm_pu" in key
        }
        buses = {k: v for k, v in results.items() if "bus" in k}
        vm_pus = {
            bus: val
            for bus, data in buses.items()
            for key, val in data.items()
            if "vm_pu" in key
        }

        checks = {}
        for bus in uvm_pus:
            vm_pu = uvm_pus[bus]
            checks[bus] = low <= vm_pu <= high

            if not checks[bus]:
                self.assertLessEqual(
                    vm_pus[bus],
                    high,
                    msg=(
                        f"Voltage of bus {bus} is above limit: {vm_pus[bus]} "
                        f"/ {high}",
                    ),
                )
                self.assertGreaterEqual(
                    vm_pus[bus],
                    low,
                    msg=(
                        f"Voltage of bus {bus} is below limit: {vm_pus[bus]} "
                        f"/ {low}",
                    ),
                )
        return checks


if __name__ == "__main__":
    unittest.main()
