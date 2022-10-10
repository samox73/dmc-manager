import pathlib
import numpy as np
import matplotlib.pyplot as plt
from manager.store import store
from manager.analyzer import E1, E2, fit_exp

clear_db = False
project_name = "order_restraint_convergence"
root_dir = "/home/samox/computing/dmcmanager"
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
runs_dir = f"{cfg_dir}/runs_1"

alpha = 1
energy_estimates = np.array(
    [
        -0.6885819,
        -0.8241995,
        -0.94908814,
        -0.98075377,
        -0.99332357,
        -1.00826087,
        -1.00303962,
        -1.00839032,
        -1.01191733,
        -1.01383529,
        -1.01513106,
        -1.01599759,
        -1.01661215,
        -1.01695265,
        -1.01697126,
        -1.01685529,
        -1.01704529,
        -1.01694835,
        -1.01706124,
        -1.01712808,
    ]
)
z_estimates = np.array(
    [
        0.83021854,
        0.74655703,
        0.69593355,
        0.66381154,
        0.64245065,
        0.62756321,
        0.61762767,
        0.61080199,
        0.6058308,
        0.60255643,
        0.60056019,
        0.59887054,
        0.59766754,
        0.59704183,
        0.59660041,
        0.59643644,
        0.59602974,
        0.5959925,
        0.595746,
        0.59574649,
    ]
)

energy_delta = 0.1
mus = energy_estimates - energy_delta
momentum = 0

max_orders = np.array(
    [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    ],
    dtype=float,
)

max_steps = np.linspace(100_000_000, 100_000_000, len(max_orders))
