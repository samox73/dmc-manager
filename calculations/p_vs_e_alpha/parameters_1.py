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
runs_dir = f"{cfg_dir}/runs_1"

alpha = 1

N = 77
momenta = np.linspace(0, 1.9, N)
# energy_estimates = -1.0168 + np.linspace(0, 1, N)
# momenta = np.array(
#     [
#     ]
# )
energy_estimates = np.array(
    [
        -1.01680734,
        -1.01670571,
        -1.01567564,
        -1.01435444,
        -1.01248631,
        -1.01008656,
        -1.00730635,
        -1.00386082,
        -1.000023,
        -0.99543667,
        -0.99060607,
        -0.98523436,
        -0.97924797,
        -0.97269248,
        -0.9657076,
        -0.95823818,
        -0.95013331,
        -0.9416243,
        -0.93267165,
        -0.92314181,
        -0.91308741,
        -0.90281218,
        -0.8917721,
        -0.88009462,
        -0.86820433,
        -0.85578333,
        -0.84277824,
        -0.82932573,
        -0.81544436,
        -0.8012715,
        -0.78649785,
        -0.77147683,
        -0.75584221,
        -0.73983813,
        -0.72320775,
        -0.70618395,
        -0.68895074,
        -0.67103509,
        -0.65314515,
        -0.63493968,
        -0.61608695,
        -0.59694444,
        -0.57754765,
        -0.55814399,
        -0.53786094,
        -0.51774905,
        -0.49710996,
        -0.47628312,
        -0.45547611,
        -0.43454835,
        -0.41331822,
        -0.39175385,
        -0.37060463,
        -0.34886267,
        -0.3278448,
        -0.30596401,
        -0.28520544,
        -0.26374094,
        -0.24270456,
        -0.22168248,
        -0.20097393,
        -0.18140882,
        -0.16057147,
        -0.14194261,
        -0.12509776,
        -0.10731353,
        -0.0911607,
        -0.07519663,
        -0.05791219,
        -0.04620948,
        -0.03671312,
        -0.02331339,
        -0.0124704,
        0.00120067,
        0.00763443,
        0.01827653,
        0.02787381,
    ]
)
e_delta = 0.1
mus = energy_estimates - e_delta

# max_steps = np.linspace(1_00_000_000, 1_00_000_000, len(momenta))
start_at = np.where(momenta > 1.5)[0][0]
max_steps = np.append(
    np.zeros(start_at),
    np.linspace(1_00_000_000, 1_00_000_000, len(momenta) - start_at),
)
