import numpy as np
from manager.store import store

project_name = "alpha_vs_e"
store = store(collection_name=project_name)
root_dir = "/home/samox/computing/dmcmanager"
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"

alphas = np.array(
    [
        0.0,
        0.5,
        1.0,
        1.5,
        2.0,
        2.5,
        3.0,
        3.5,
        4.0,
        4.5,
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.5,
        8.0,
    ]
)
energy_estimates = np.array(
    [
        0.0,
        -0.5040475,
        -1.016751,
        -1.53909345,
        -2.07059473,
        -2.61430367,
        -3.17027431,
        -3.74018507,
        -4.32353754,
        -4.92977316,
        -5.55315404,
        -6.201265,
        -6.87686343,
        -7.57231497,
        -8.31887697,
        -9.11692791,
        -9.92403001,
    ]
)
mus = energy_estimates - 0.05

max_steps = np.linspace(1_000_000, 1_000_000, len(alphas))
momentum = 0
