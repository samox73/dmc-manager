from manager.json_parser import fft_to_json, run_properties_to_json
from manager.store import store
from manager.run_executor import run_executor
from manager.factory.multi_config import *

import numpy as np
from time import sleep

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.rcsetup as rcsetup

print(rcsetup.all_backends)
matplotlib.use("Agg", force=True)

store = store()
reset = False
# reset = False

# ============= RESET STORE ============
if reset:
    c = store.collection.delete_many({})
    print(f"Deleted {c.deleted_count} documents from the store")

# ============= SIMULATION =============
cfg_dir = "/home/samox/computing/dmcmanager/examples/multi_config_template"
cfg_template_path = f"{cfg_dir}/default_config.json"
run_dir = f"{cfg_dir}/runs"

configs = multi_config()
configs.alphas(np.linspace(1.0, 2, 1)).momenta(np.linspace(0, 1.2, 6)).max_steps(
    100000000
).build(cfg_template_path)

executor = run_executor().configs(configs).run_dir(run_dir).store(store)

if reset:
    executor.initialize(reset=True)
    executor.run("mpirun -c 12 dmc")
else:
    executor.initialize(reset=False)


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
    return {"run_properties": run_properties, "fft": fft}


if reset:
    executor.save(function=save_func)

# ============= RETRIEVAL =============
filter = {"run_properties.alpha_": 1}
results = store.collection.find(filter)
count = store.collection.count_documents(filter)
print(f"Found {count} documents with filter {filter}")

fig, ax = plt.subplots(1, count, figsize=(count * 4, 4))
ax = ax if hasattr(ax, "__getitem__") else [ax]

for i, result in zip(range(count), results):
    fft = result["fft"]
    properties = result["run_properties"]
    alpha = properties["alpha_"]
    ax[i].plot(fft["taus"], fft["G_t"], label=f"alpha = {alpha}")
    ax[i].legend()

os.chdir(cfg_dir)
plt.savefig("plot.png")
