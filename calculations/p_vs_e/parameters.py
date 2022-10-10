import pathlib
import numpy as np
import matplotlib.pyplot as plt
from manager.store import store
from manager.analyzer import E1, E2, fit_exp

clear_db = False
project_name = "p_vs_e"
store = store(collection_name=project_name)
root_dir = "/home/samox/computing/dmcmanager"
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
runs_dir = f"{cfg_dir}/runs"

alpha = 1

# momenta = np.concatenate(
#     (
#         np.linspace(1, 1.3, 6, endpoint=False),
#         np.linspace(1.3, 1.8, 5),
#     )
# )
# energy_estimates = (momenta - 1) / 0.8 * 0.62 - 0.62
# mus = energy_estimates - 0.1

momenta = np.array(
    [
        0.001,
        0.04096,
        0.08092,
        0.12088,
        0.16084,
        0.2008,
        0.24076,
        0.28072,
        0.32068,
        0.36064,
        0.4006,
        0.44056,
        0.48052,
        0.52048,
        0.56044,
        0.6004,
        0.64036,
        0.68032,
        0.72028,
        0.76024,
        0.8002,
        0.84016,
        0.88012,
        0.92008,
        0.96004,
        1.0,
        1.05,
        1.1,
        1.15,
        1.2,
        1.25,
        1.3,
        1.425,
        1.55,
        1.675,
        1.8,
        1.825,
        1.85,
        1.875,
        1.9,
        2,
    ]
)
energy_estimates = np.array(
    [
        -1.01673988,
        -1.01604701,
        -1.01397533,
        -1.01061934,
        -1.00592729,
        -0.99994615,
        -0.99256575,
        -0.98386805,
        -0.97386707,
        -0.96258852,
        -0.94992331,
        -0.93612054,
        -0.92095431,
        -0.90448879,
        -0.88677122,
        -0.86785991,
        -0.84769552,
        -0.82637182,
        -0.80386358,
        -0.7801885,
        -0.75544616,
        -0.72955993,
        -0.70261378,
        -0.67463477,
        -0.64572267,
        -0.61719375,
        -0.57902425,
        -0.53950133,
        -0.49805883,
        -0.45764274,
        -0.41546792,
        -0.37197158,
        -0.26582095,
        -0.16236885,
        -0.07095183,
        -0.02723095,
        0,
        0,
        0,
        0,
        0,
    ]
)
mus = energy_estimates - 0.05

max_steps = np.append(
    np.zeros(len(momenta) - 5), np.linspace(100_000_000, 100_000_000, 5)
)
