import pathlib
import numpy as np
import matplotlib.pyplot as plt
from manager.store import store


project_name = "p_vs_e"
store = store(collection_name=project_name)
root_dir = pathlib.Path().resolve()
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"
N = 3
momenta = np.geomspace(0, 1.8, N)
mus = np.geomspace(-1.1, -1.1, N)
max_steps = np.linspace(10_000_000, 20_000_000, N)
alpha = 1
