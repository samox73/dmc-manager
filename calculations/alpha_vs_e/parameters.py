import pathlib
import numpy as np
import matplotlib.pyplot as plt
from manager.store import store


project_name = "alpha_vs_e"
store = store(collection_name=project_name)
root_dir = pathlib.Path().resolve()
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"
N = 100
alphas = np.linspace(0.001, 6, N)
mus = np.linspace(-0.1, -6.9, N)
max_steps = np.linspace(200_000_000, 600_000_000, N)
momentum = 0
