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
runs_dir = f"{cfg_dir}/runs_3"

alpha = 3
energy_estimates = np.array(
    [
        -1.7940916,
        -2.21461219,
        -2.44063278,
        -2.59032375,
        -2.69422724,
        -2.77239969,
        -2.83350488,
        -2.88255624,
        -2.95481176,
        -3.00410951,
        -3.04010235,
        -3.06668326,
        -3.08656052,
        -3.1026623,
        -3.12871164,
        -3.1433244,
        -3.15261938,
        -3.15801194,
        -3.16202201,
        -3.16358418,
        -3.16676978,
        -3.16801978,
        -3.16836326,
    ]
)
z_estimates = np.array(
    [
        0.78379505,
        0.65619901,
        0.56861189,
        0.50449362,
        0.45664012,
        0.41900369,
        0.38875649,
        0.36384383,
        0.32564997,
        0.29751932,
        0.27622438,
        0.25946158,
        0.24617095,
        0.23507799,
        0.21508611,
        0.20271138,
        0.19450625,
        0.18835656,
        0.18330254,
        0.18035688,
        0.17482841,
        0.17312274,
        0.17231744,
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
        10,
        12,
        14,
        16,
        18,
        20,
        25,
        30,
        35,
        40,
        45,
        50,
        60,
        70,
        80,
    ],
    dtype=float,
)

max_steps = np.linspace(10_000_000, 10_000_000, len(max_orders))
