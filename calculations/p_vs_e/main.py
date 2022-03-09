from manager.analyzer import E0, fit_exp, E2
from manager.json_parser import fft_to_json, run_properties_to_json
from manager.store import store
from manager.run_executor import run_executor
from manager.factory.multi_config import *

import numpy as np
from time import sleep
import pathlib
import matplotlib.pyplot as plt

reset = False

# ============= SIMULATION =============
root_dir = pathlib.Path().resolve()
project_name = "p_vs_e"
cfg_dir = f"{root_dir}/calculations/{project_name}"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"

configs = multi_config()
configs.momenta(np.linspace(0, 1.6, 13)).max_steps(100_000_000).build(cfg_template_path)

store = store()
executor = run_executor().configs(configs).run_dir(run_dir).store(store)

executor.initialize(reset=reset)
if reset:
    delete_filter = {"tags.project": project_name}
    c = store.collection.delete_many(delete_filter)
    print(f"Deleted {c.deleted_count} documents from the store")
    executor.run("mpirun -c 12 dmc")


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
    tags = {"project": project_name}
    return {"run_properties": run_properties, "fft": fft, "tags": tags}


if reset:
    executor.save(function=save_func)

# ============= RETRIEVAL =============
filter = {"run_properties.alpha_": 1, "tags.project": project_name}
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
plt.savefig("plot.png", bbox_inches="tight")
