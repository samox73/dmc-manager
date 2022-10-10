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
runs_dir = f"{cfg_dir}/runs_5"

alpha = 5
energy_estimates = np.array(
    [
        -4.10286395,
        -4.65020378,
        -4.91744676,
        -5.07820973,
        -5.18266541,
        -5.25703806,
        -5.31426321,
        -5.36242386,
        -5.39453654,
        -5.41583142,
        -5.43319917,
        -5.4527117,
        -5.48227417,
        -5.50594932,
        -5.52452776,
        -5.54015126,
        -5.55040626,
        -5.54998364,
        -5.5511204,
        -5.55268552,
        -5.55263736,
    ]
)
z_estimates = np.array(
    [
        0.39573374,
        0.25950751,
        0.19151526,
        0.15250428,
        0.12984447,
        0.11577972,
        0.09822224,
        0.08175838,
        0.07328481,
        0.07173524,
        0.08309858,
        0.08342749,
        0.06708147,
        0.05324511,
        0.04393677,
        0.03691803,
        0.03297268,
        0.03303416,
        0.03270792,
        0.03219452,
        0.03217592,
    ]
)

energy_delta = 0.1
mu = energy_estimates - energy_delta
momentum = 0

max_orders = np.array(
    [
        5,
        10,
        15,
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
        90,
        100,
        120,
        140,
        160,
        180,
        200,
        250,
    ],
    dtype=float,
)

max_steps = np.linspace(20_000_000, 20_000_000, len(max_orders))
