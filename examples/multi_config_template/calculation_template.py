from time import sleep
from manager.factory.multi_config import *
import numpy as np
import matplotlib.pyplot as plt

from manager.run_executor import run_executor
from manager.store import store

store = store()

# ============= SIMULATION =============
reset = False
configs = multi_config()

configs.alphas(
    np.linspace(1, 2, 2)).momenta(
    np.linspace(0, 1, 2)).build()

run_dir = "/home/samox/computing/dmcmanager/examples/multi_config_template/runs"
executor = run_executor().configs(configs).run_dir(run_dir).store(store)

if reset:
    executor.initialize(reset=True)
    executor.run("dmc")
else:
    executor.initialize(reset=False)


# ============= SAVING =============
executor.save()

# ============= RETRIEVAL =============
filter = {
    "run_properties.alpha_": 1
}
results = store.collection.find(filter)
count = store.collection.count_documents(filter)
print(f"Found {count} documents with filter {filter}")

fig, ax = plt.subplots(1, count, figsize=(count*4, 4))
for i, result in zip(range(count), results):
    fft = result["fft"]
    properties = result["run_properties"]
    alpha = properties["alpha_"]
    ax[i].plot(fft["taus"], fft["G_t"], label=f"alpha = {alpha}")
    ax[i].legend()

# ============= RESET STORE ============
c = store.collection.delete_many({})
print(f"Deleted {c.deleted_count} documents from the store")
