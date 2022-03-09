import pathlib
from manager.analyzer import E0, E2, fit_exp
from manager.json_parser import fft_to_json, run_properties_to_json
from manager.store import store
from manager.run_executor import run_executor
from manager.factory.easy_config import *

import numpy as np
import matplotlib.pyplot as plt

store = store(collection_name="examples")

# ============= RESET STORE ============
c = store.collection.delete_many({})
print(f"Deleted {c.deleted_count} documents from the store")

# ============= SIMULATION =============
root_dir = pathlib.Path().resolve()
project_name = "easy_template"
cfg_dir = f"{root_dir}/examples/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"

# specify all arguments
easy_config = easy_config()
easy_config.get_default_input(cfg_template_path)
alpha = 1
momenta = np.linspace(0, 1.4, 10)
max_steps = 10_000_000

# iterate over all iterable arguments
configs = []
for momentum in momenta:
    # build the patch object
    patch = {
        "/Configuration/alpha": alpha,
        "/Configuration/momentum": momentum,
        "/Simulation/max_steps": max_steps,
        "/Simulation/max_time": 999_999_999,
    }
    # generate and save the config in an array
    config = easy_config.generate(**patch)
    configs.append(config)

executor = run_executor().configs(configs).run_dir(run_dir).store(store)
executor.initialize(clear=True)

# specify the executable just like you would in a terminal
executor.run("mpirun -c 12 dmc")

# saving and plotting is completely optional, but relies on a running mongoDB server
# you can customize the the url when initializing the store
# ============= SAVING =============
def save_func():
    fft_raw = fft_to_json()
    fft = {
        "taus": fft_raw["tau"],
        "G0_t": fft_raw["G0_t"],
        "S_higher_t": fft_raw["S_higher_t"],
        "G_w": fft_raw["G_w"],
        "G_t": fft_raw["G_t"],
    }
    run_properties = run_properties_to_json()
    return {"run_properties": run_properties, "fft": fft, "tags": project_name}


executor.save(function=save_func)

# ============= RETRIEVAL =============
filter = {"run_properties.alpha_": alpha, "tags": project_name}
results = store.collection.find(filter)

fig, ax = plt.subplots(1, 2, figsize=(17, 7))

energies = []
momenta = []
z_values = []
for result in results:
    fft = result["fft"]
    taus = np.array(fft["taus"])
    G_t = np.array(fft["G_t"])
    properties = result["run_properties"]
    z, e = fit_exp(taus, G_t, properties)
    momenta.append(properties["p_modulus_"])
    energies.append(e)
    z_values.append(z)

momenta_fine = np.linspace(0, 1.4, 1000)
ax[0].plot(momenta, energies, label=f"E")
ax[0].plot(momenta_fine, E0(momenta_fine, 1), linestyle="--", label="E0")
ax[0].plot(momenta_fine, E2(momenta_fine, 1), linestyle="--", label="E2")
ax[0].legend()
ax[1].plot(momenta, z_values, label=f"Z")
ax[1].legend()
os.chdir(cfg_dir)
plt.savefig("plot.png")
