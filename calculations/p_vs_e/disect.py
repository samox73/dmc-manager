import shutil
from manager.factory.easy_config import easy_config
from manager.json_parser import file_to_json, string_to_file
import numpy as np
import json
import os
import subprocess
from parameters import runs_dir, cfg_template_path


def gen_run_dir(config_):
    cfg_ = json.loads(config_)["Configuration"]
    msr_ = json.loads(config_)["Measurements"]
    p_ = cfg_["momentum"]
    mu_ = cfg_["mu"]
    e_ = msr_["energy"]["estimate"]
    idx_ = f"p_{p_}"
    # idx_ = f"p_{p_}-mu_{mu_}-e_{e_}"
    return f"run-{idx_}"


def gen_new_config(e_result_, e_delta_):
    cfg_ = easy_config()
    cfg_.get_default_input(os.getcwd() + "/input.json")
    patch_ = {
        "/Measurements/energy/estimate": e_result_,
        "/Measurements/energy/delta": e_delta_ / 1.1,
        "/Configuration/mu": e_result_ + e_delta_,
    }
    config_ = cfg_.generate(**patch_)
    string_to_file(config_, "input.json")


def setup(run_dir_, config_):
    try:
        os.mkdir(run_dir_)
    except Exception as e:
        print(f"Got error: {e}")
    os.chdir(run_dir_)
    with open("input.json", "w") as input_file_:
        input_file_.write(config_)


def run():
    converged = False
    index = 0
    e_input = 0
    e_result = 100000
    while not converged:
        index += 1
        print(f"\t{index = }\t{e_result = :.5f}")
        with open("log.txt", "w") as log_:
            subprocess.run("mpirun -c 14 dmc".split(), stderr=subprocess.STDOUT, stdout=log_)
        e_input = float(file_to_json("input.json")["Measurements"]["energy"]["estimate"])
        e_delta = float(file_to_json("input.json")["Measurements"]["energy"]["delta"])
        e_result = float(file_to_json("out_jackknife.json")["E"]["estimate"])
        err = abs(e_input - e_result)
        if err < 0.0001:
            print(f"\tconvergence reached with err={err}")
            converged = True
        elif err > 2:
            print(f"\tdiverging energy, aborting (err={err})")
            converged = True
        else:
            gen_new_config(e_result, e_delta)



n = 2
momenta = np.linspace(0, 1.8, n)
e_estimates = np.linspace(-1.1, 0.0, n)
mus = np.linspace(-1.1, 0.1, n)
steps = np.linspace(100_000_000, 100_000_000, 3)

ez_config = easy_config()
ez_config.get_default_input(cfg_template_path)
configs = []
print(f"\tmomentum\tmu\t\tE")
print(f"\t--------------")
for momentum, mu, e_estimate in zip(momenta, mus, e_estimates):
    print(f"\t{momentum:.4f}\t\t{mu:.4f}\t{e_estimate:.4f}")
    # build the patch object
    patch = {
        "/Configuration/momentum": momentum,
        "/Measurements/energy/estimate": e_estimate,
        "/Configuration/mu": mu,
        "/Simulation/max_steps": steps[0],
        "/Simulation/max_time": 999_999_999,
    }
    # generate and save the config in an array
    config = ez_config.generate(**patch)
    configs.append(config)

shutil.rmtree(runs_dir, ignore_errors=True)
try:
    os.mkdir(runs_dir)
except Exception as e:
    print(e)

os.chdir(runs_dir)
print(runs_dir)

configs_done = []
for config in configs:
    run_dir = gen_run_dir(config)
    setup(run_dir, config)
    print(f"starting runs for {run_dir}")
    run()
    configs_done.append(config)
    os.chdir(runs_dir)