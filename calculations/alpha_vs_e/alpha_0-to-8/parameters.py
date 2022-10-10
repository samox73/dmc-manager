import numpy as np
from manager.store import store


project_name = "alpha_vs_e"
store = store(collection_name=project_name)
root_dir = "/home/samox/computing/dmcmanager"
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"
N = 17

# alphas = np.linspace(0, 8, N)
# mus = np.linspace(-0.1, -10, N)
# energy_estimates = np.linspace(-0.1, -10, N)

alphas = np.array([0. , 0.5, 1. , 1.5, 2. , 2.5, 3. , 3.5, 4. , 4.5, 5. , 5.5, 6. , 6.5, 7. ,
 7.5, 8. ])
energy_estimates = np.array([ 0.        , -0.50393657, -1.01580266, -1.5368346 , -2.06874657,
 -2.61375542, -3.16347561, -3.73983327, -4.33009022, -4.92506787,
 -5.54717603, -6.20209514, -6.87966779, -7.57882435, -8.27918566,
 -9.09737379, -9.93468202])
mus = energy_estimates - 0.05

max_steps = np.linspace(2_000_000, 10_000_000, N)
momentum = 0
