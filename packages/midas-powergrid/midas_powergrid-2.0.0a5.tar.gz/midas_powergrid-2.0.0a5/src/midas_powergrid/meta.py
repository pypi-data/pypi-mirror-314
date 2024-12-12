"""This module contains the mosaik meta definition for the
pandapower simulator.

"""

import numpy as np

ATTRIBUTE_MAP = {
    "Bus": {
        "bus": [
            ("in_service", "bool", 0, 2),  # bus is operational
            ("vn_kv", "float", 0, 440),  # nominal voltage
        ],
        "res_bus": [
            ("p_mw", "float", -np.inf, np.inf),  # active power
            ("q_mvar", "float", -np.inf, np.inf),  # reactive power
            ("vm_pu", "float", 0.0, 1.2),  # voltage magnitude
            ("va_degree", "float", -180.0, 180.0),  # voltage angle
        ],
    },
    "Line": {
        "line": [
            ("in_service", "bool", 0, 2),  # line is operational
            ("max_i_ka", "float", 0, np.inf),  # maximum current
        ],
        "res_line": [
            ("loading_percent", "float", 0, np.inf),  # utilization
            ("p_from_mw", "float", -np.inf, np.inf),  # active power from
            ("p_to_mw", "float", -np.inf, np.inf),  # active power to
            ("q_from_mvar", "float", -np.inf, np.inf),  # reactive power from
            ("q_to_mvar", "float", -np.inf, np.inf),  # reactive power to
            ("vm_from_pu", "float", 0.0, np.inf),  # voltage magnitude from
            ("vm_to_pu", "float", 0.0, np.inf),  # voltage magnitude to
            ("va_from_degree", "float", -180.0, 180.0),  # voltage angle from
            ("va_to_degree", "float", -180.0, 180.0),  # voltage angle to
            ("i_from_ka", "float", -np.inf, np.inf),  # current from
            ("i_to_ka", "float", -np.inf, np.inf),  # current to
        ],
    },
    "Trafo": {
        "trafo": [
            ("in_service", "bool", 0, 2),  # trafo is operational
            ("tap_pos", "int", -np.inf, np.inf),  # position of tap changer
            ("tap_min", "int", -np.inf, np.inf),  # minimal tap position
            ("tap_max", "int", -np.inf, np.inf),  # maximum tap position
        ],
        "res_trafo": [
            ("loading_percent", "float", 0, np.inf),  # utilization
            ("p_hv_mw", "float", -np.inf, np.inf),  # active power hv
            ("p_lv_mw", "float", -np.inf, np.inf),  # active power lv
            ("q_hv_mvar", "float", -np.inf, np.inf),  # reactive power hv
            ("q_lv_mvar", "float", -np.inf, np.inf),  # reactive power lv
            ("vm_hv_pu", "float", 0.0, np.inf),  # voltage magnitude hv
            ("vm_lv_pu", "float", 0.0, np.inf),  # voltage magnitude lv
            ("va_hv_degree", "float", -180.0, 180.0),  # voltage angle hv
            ("va_lv_degree", "float", -180.0, 180.0),  # voltage angle lv
            ("i_hv_ka", "float", -np.inf, np.inf),  # current hv
            ("i_lv_ka", "float", -np.inf, np.inf),  # current lv
        ],
    },
    "Switch": {
        "switch": [("closed", "bool", 0, 2)],
        "res_switch": [("i_ka", "float", -np.inf, np.inf)],
    },
    "Ext_grid": {
        "ext_grid": [],
        "res_ext_grid": [
            ("p_mw", "float", -np.inf, np.inf),  # active power
            ("q_mvar", "float", -np.inf, np.inf),  # reactive power
        ],
    },
    "Load": {
        "load": [
            ("p_mw", "float", -np.inf, np.inf),  # active power
            ("q_mvar", "float", -np.inf, np.inf),  # reactive power
            ("in_service", "bool", 0, 2),  # load is operational
        ],
        "res_load": [],
    },
    "Sgen": {
        "sgen": [
            ("p_mw", "float", -np.inf, np.inf),  # active power
            ("q_mvar", "float", -np.inf, np.inf),  # reactive power
            ("in_service", "bool", 0, 2),  # generator is operational
        ],
        "res_sgen": [],
    },
    "Storage": {
        "storage": [
            ("p_mw", "float", -np.inf, np.inf),  # active power
            ("q_mvar", "float", -np.inf, np.inf),  # reactive power
            ("in_service", "bool", 0, 2),  # storage is operational
        ],
        "res_storage": [],
    },
}
META = {
    "type": "time-based",
    "models": {
        "Grid": {
            "public": True,
            "params": [
                "gridfile",  # Name of the grid topology
                "pp_params",
                "plotting",  # Flag to activate plotting
                "use_constraints",  # Flag to activate constraints
                "constraints",  # A list of constraints to activate
                "actuator_multiplier",
                "include_slack_bus",
            ],
            "attrs": ["health", "grid_json"],
        },
        "Ext_grid": {
            "public": False,
            "params": [],
            "attrs": [
                attr[0] for attr in ATTRIBUTE_MAP["Ext_grid"]["ext_grid"]
            ]
            + [attr[0] for attr in ATTRIBUTE_MAP["Ext_grid"]["res_ext_grid"]],
            # "attrs": [
            #     "p_mw",  # load active power [MW]
            #     "q_mvar",  # load reactive power [MVAr]
            # ],
        },
        "Bus": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Bus"]["bus"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Bus"]["res_bus"]],
            # "attrs": [
            #     "p_mw",  # load Active power [MW]
            #     "q_mvar",  # Reactive power [MVAr]
            #     "vn_kv",  # Nominal bus voltage [KV]
            #     "vm_pu",  # Voltage magnitude [p.u]
            #     "va_degree",  # Voltage angle [deg]
            #     "in_service",  # Bus is in service [bool]
            # ],
        },
        "Load": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Load"]["load"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Load"]["res_load"]],
            # "attrs": [
            #     "p_mw",  # load Active power [MW]
            #     "q_mvar",  # Reactive power [MVAr]
            #     "in_service",  # specifies if the load is in service.
            #     "controllable",  # States if load is controllable or not.
            # ],
        },
        "Sgen": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Sgen"]["sgen"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Sgen"]["res_sgen"]],
            # "attrs": [
            #     "p_mw",  # load Active power [MW]
            #     "q_mvar",  # Reactive power [MVAr]
            #     "in_service",  # specifies if the load is in service.
            #     "controllable",  # States if load is controllable or not.
            #     "va_degree",  # Voltage angle [deg]
            # ],
        },
        "Trafo": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Trafo"]["trafo"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Trafo"]["res_trafo"]],
            # "attrs": [
            #     "p_hv_mw",  # Active power at "from" side [MW]
            #     "q_hv_mvar",  # Reactive power at "from" side [MVAr]
            #     "p_lv_mw",  # Active power at "to" side [MW]
            #     "q_lv_mvar",  # Reactive power at "to" side [MVAr]
            #     "sn_mva",  # Rated apparent power [MVA]
            #     "max_loading_percent",  # Maximum Loading
            #     "vn_hv_kv",  # Nominal primary voltage [kV]
            #     "vn_lv_kv",  # Nominal secondary voltage [kV]
            #     "vm_hv_pu",
            #     "vm_lv_pu",
            #     "va_hv_degree",
            #     "va_lv_degree",
            #     "pl_mw",  # Active power loss [MW]
            #     "ql_mvar",  # reactive power consumption of the
            #     # transformer [Mvar]
            #     # 'pfe_kw',       #  iron losses in kW [kW]
            #     # 'i0_percent',       #  iron losses in kW [kW]
            #     "loading_percent",  # load utilization relative to rated
            #     # power [%]
            #     "i_hv_ka",  # current at the high voltage side of the
            #     # transformer [kA]
            #     "i_lv_ka",  # current at the low voltage side of the
            #     # transformer [kA]
            #     "tap_max",  # maximum possible  tap turns
            #     "tap_min",  # minimum possible tap turns
            #     "tap_pos",  # Currently active tap turn
            #     "in_service",  # Specifies if the trafo is in service
            # ],
        },
        "Line": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Line"]["line"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Line"]["res_line"]],
            # "attrs": [
            #     "p_from_mw",  # Active power at "from" side [MW]
            #     "q_from_mvar",  # Reactive power at "from" side [MVAr]
            #     "p_to_mw",  # Active power at "to" side [MW]
            #     "q_to_mvar",  # Reactive power at "to" side [MVAr]
            #     "max_i_ka",  # Maximum current [KA]
            #     "length_km",  # Line length [km]
            #     "pl_mw",  # active power losses of the line [MW]
            #     "ql_mvar",  # reactive power consumption of the line [MVar]
            #     "i_from_ka",  # Current at from bus [kA]
            #     "i_to_ka",  # Current at to bus [kA]
            #     "loading_percent",  # line loading [%]
            #     "r_ohm_per_km",  # Resistance per unit length [Ω/km]
            #     "x_ohm_per_km",  # Reactance per unit length [Ω/km]
            #     "c_nf_per_km",  # Capactity per unit length [nF/km]
            #     "in_service",  # Boolean flag (True|False)
            #     "vm_from_pu",
            #     "vm_to_pu",
            #     "va_from_degree",
            #     "va_to_degree",
            # ],
        },
        "Switch": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Switch"]["switch"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Switch"]["res_switch"]],
            # "attrs": [
            #     "et",
            #     "type",
            #     "closed",
            # ],
        },
        "Storage": {
            "public": False,
            "params": [],
            "attrs": [attr[0] for attr in ATTRIBUTE_MAP["Storage"]["storage"]]
            + [attr[0] for attr in ATTRIBUTE_MAP["Storage"]["res_storage"]],
            # "attrs": [
            #     "p_mw",  # load Active power [MW]
            #     "q_mvar",  # Reactive power [MVAr]
            #     "max_e_mwh",  # maximum charge level
            #     "in_service",  # specifies if the load is in service.
            #     "controllable",  # States if load is controllable or not.
            # ],
        },
    },
}
