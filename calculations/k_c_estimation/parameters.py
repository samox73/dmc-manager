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

alpha = 0

N = 11
momenta = np.append(np.array([0]), np.linspace(1.4, 1.9, N))
energy_estimates = -1.0168 + np.linspace(0, 1, N)
e_delta = 0.2
mus = energy_estimates - e_delta

max_steps = np.linspace(1_000_000_000, 1_000_000_000, len(momenta))
