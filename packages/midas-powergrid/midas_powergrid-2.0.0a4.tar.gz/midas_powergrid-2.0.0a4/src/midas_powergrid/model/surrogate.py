import csv
import os
from os.path import join

import joblib
import numpy as np

from .pp_grid import PPGrid


class SurrogateGrid(PPGrid):
    def __init__(self, grid_name, grid_params):
        surrogate_params = grid_params.pop("surrogate_params")
        super().__init__(grid_name, grid_params)

        base_path = surrogate_params["base_path"]
        self._model = joblib.load(
            join(base_path, surrogate_params["model_path"])
        )
        self._x_scaler = joblib.load(
            join(base_path, surrogate_params["x_scaler"])
        )
        self._y_scaler = joblib.load(
            join(base_path, surrogate_params["y_scaler"])
        )
        self._input_map = joblib.load(
            join(base_path, surrogate_params["input_map"])
        )
        self._output_map = joblib.load(
            join(base_path, surrogate_params["output_map"])
        )
        self._evaluate = (
            True
            if surrogate_params.get("evaluate", "true") == "true"
            else False
        )
        self._save_path = surrogate_params.get("save_path", ".")
        self._model_result_path = join(
            self._save_path,
            surrogate_params.get("save_model_results_to", "model_results.csv"),
        )
        self._ppg_results_path = join(
            self._save_path,
            surrogate_params.get("save_ppgrid_results_to", "ppg_results.csv"),
        )

        self._inputs = np.zeros((len(self._input_map),))
        self._outputs = np.zeros((len(self._output_map),))
        self._rmses = {
            "vm_pu": [],
            "va_degree": [],
            "bus_p_mw": [],
            "bus_q_mvar": [],
            "line_loading": [],
            "trafo_loading": [],
            "eg_p_mw": [],
            "eg_q_mvar": [],
        }
        self._model_results = []
        self._ppg_results = []

    def set_value(self, etype, idx, attr, val):
        key = f"{etype.capitalize()}_{idx:03d}__{attr}"
        self._inputs[self._input_map[key]] = val

        if self._evaluate:
            super().set_value(etype, idx, attr, val)

    def run_powerflow(self):
        self._outputs = self._y_scaler.inverse_transform(
            self._model.predict(
                self._x_scaler.transform(self._inputs.reshape(1, -1))
            )
        )[0]
        if self._inputs.sum() == 0.0 or self._evaluate:
            super().run_powerflow()

        if self._evaluate:
            self._model_results.append(list(self._outputs))
            self._ppg_results.append(
                list(self._grid.res_bus.vm_pu.values[1:])
                + list(self._grid.res_bus.va_degree.values[1:])
                + list(self._grid.res_bus.p_mw.values[1:])
                + list(self._grid.res_bus.q_mvar.values[1:])
                + list(self._grid.res_line.loading_percent.values)
                + list(self._grid.res_trafo.loading_percent.values)
                + list(self._grid.res_ext_grid.p_mw.values)
                + list(self._grid.res_ext_grid.q_mvar.values)
            )

    def get_value(self, etype, idx=None, attr=None):
        if idx is not None and attr is not None:
            key = f"{etype.capitalize()}_{idx:03d}__{attr}"
            if key in self._input_map:
                return self._inputs[self._input_map[key]]
            elif key in self._output_map:
                return self._outputs[self._output_map[key]]
            else:
                return super().get_value(etype, idx, attr)
        elif attr is not None:
            keys = [
                k
                for k in self._input_map
                if (etype.capitalize() in k and attr in k)
            ]
            if keys:
                return [self._inputs[self._input_map[k]] for k in keys]
            keys = [
                k
                for k in self._output_map
                if (etype.capitalize() in k and attr in k)
            ]
            if keys:
                return [self._output[self._output_map[k]] for k in keys]

        return super().get_value(etype, idx, attr)

    def finalize(self):
        if self._evaluate:
            with open(
                join(os.getcwd(), self._model_result_path), "w", newline=None
            ) as csv_file:
                writer = csv.writer(
                    csv_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )

                writer.writerow(list(self._output_map.keys()))
                for idx in range(len(self._model_results)):
                    row = self._model_results[idx]
                    writer.writerow(row)

            with open(
                join(os.getcwd(), self._ppg_results_path), "w", newline=None
            ) as csv_file:
                writer = csv.writer(
                    csv_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )

                writer.writerow(list(self._output_map.keys()))
                for idx in range(len(self._ppg_results)):
                    row = self._ppg_results[idx]
                    writer.writerow(row)

            # print(self._rmses)
            # print(
            #     f"VM PU: {np.average(self._rmses['vm_pu'])} VA Degree: "
            #     f"{np.average(self._rmses['va_degree'])} "
            # )


def rmse(v_true, v_pred):
    return np.sqrt((v_true - v_pred) ** 2)
