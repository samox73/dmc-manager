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
runs_dir = f"{cfg_dir}/runs_5"

alpha = 5

N = 21
momenta = np.array(
    [
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
        1.25,
        1.5,
        1.75,
        2.0,
        2.25,
        2.5,
        2.75,
        3.0,
        3.25,
        3.5,
        3.75,
        4.0,
        4.25,
        4.5,
        4.75,
        5.0,
    ]
)
energy_estimates = np.array(
    [
        -5.54833393,
        -5.54019773,
        -5.51129302,
        -5.47229173,
        -5.42006995,
        -5.36003941,
        -5.29292271,
        -5.22573632,
        -5.16038617,
        -5.09086095,
        -5.02562994,
        -4.95977967,
        -4.91214433,
        -4.84029781,
        -4.7801567,
        -4.73732115,
        -4.66758168,
        -4.63200467,
        -4.59404046,
        -4.55651028,
        -4.51024353,
    ]
)
e_delta = 0.1
mus = energy_estimates - e_delta

max_steps = np.linspace(6_000_000_000, 6_000_000_000, len(momenta))
