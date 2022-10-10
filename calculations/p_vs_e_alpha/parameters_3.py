import pathlib
import numpy as np
import matplotlib.pyplot as plt
from manager.store import store
from manager.analyzer import E1, E2, fit_exp

clear_db = False
project_name = "p_vs_e_alpha"
store = store(collection_name=project_name)
root_dir = "/home/samox/computing/dmcmanager"
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
runs_dir = f"{cfg_dir}/runs_3"

alpha = 3

N = 31
momenta = np.linspace(0, 3, N)
# energy_estimates = -3.17 + np.linspace(0, 1, N)
# momenta = np.array(
#     [
#     ]
# )
energy_estimates = np.array(
    [
        -3.15622307,
        -3.15433546,
        -3.14729051,
        -3.13510955,
        -3.11745393,
        -3.09529298,
        -3.06740531,
        -3.03498584,
        -2.99951681,
        -2.95929608,
        -2.91704157,
        -2.87166912,
        -2.82405409,
        -2.7755346,
        -2.72577024,
        -2.67671938,
        -2.6277598,
        -2.57868975,
        -2.53216038,
        -2.485167,
        -2.44103225,
        -2.40149484,
        -2.36141223,
        -2.32075313,
        -2.28952357,
        -2.25471998,
        -2.22211296,
        -2.19423709,
        -2.16895922,
        -2.14797205,
        -2.13552043,
    ]
)
e_delta = 0.1
mus = energy_estimates - e_delta

#max_steps = np.linspace(2_000_000_000, 2_000_000_000, len(momenta))
start_at = np.where(momenta > 1.9)[0][0]
max_steps = np.append(
    np.zeros(start_at),
    np.linspace(2_000_000_000, 2_000_000_000, len(momenta) - start_at),
)
