from cProfile import label
import os
from calculations.utils import build_color_linecollection
from manager.analyzer import E1, E2, fit_exp
from parameters import *
from matplotlib.colors import ListedColormap, BoundaryNorm

# ============= RETRIEVAL =============

filter = {
    "run_properties.alpha": alpha,
    "tags.project": project_name,
    # "run_properties.steps_done_total": {"$gt": 2_500_000_000},
}
results = store.collection.find(filter)
N = store.collection.count_documents(filter)
print(f"retrieved {N} documents with filter {filter}")

fig, ax = plt.subplots(1, 3, figsize=(20, 6))

z_estimates = np.linspace(0.6, 0, N)
energies = []
momenta = []
z_values = []
steps_done_total = []
print(f"\tmomentum\t\tE\t\tZ")
print(f"\t----------------------------------------")
for z_estimate, result in zip(z_estimates, results):
    fft = result["fft"]
    taus = np.array(fft["taus"])
    G_t = np.array(fft["G_t"])
    properties = result["run_properties"]
    momentum = properties["momentum"]
    z, e = fit_exp(
        taus,
        G_t,
        properties,
        z_estimate=z_estimate,
        e_estimate=properties["mu"],
    )
    print(f"\t{momentum:.4f}\t\t{e:.4f}\t\t{z:.4f}")
    momenta.append(momentum)
    steps_done_total.append(properties["steps_done_total"])
    energies.append(e)
    z_values.append(z)
    ax[2].plot(taus, G_t)

momenta_fine = np.linspace(0, 1.4, 1000)
momenta = np.array(momenta)
energies = np.array(energies)
z_values = np.array(z_values)
steps_done_total = np.array(steps_done_total)

ax[0].plot(
    momenta_fine,
    E1(momenta_fine, alpha),
    linestyle="dashdot",
    color="#343400",
    label="E1",
)
ax[0].plot(
    momenta_fine,
    E2(momenta_fine, alpha),
    linestyle="dashed",
    color="#343400",
    label="E2",
)

paddingx = 0.1
paddingy = 0.05
lc = build_color_linecollection(momenta, energies, steps_done_total)
line = ax[0].add_collection(lc)
fig.colorbar(line, ax=ax[0])
ax[0].set_xlim(momenta.min() - paddingx, momenta.max() + paddingx)
ax[0].set_ylim(energies.min() - paddingy, energies.max() + paddingy)
ax[0].legend()

lc = build_color_linecollection(momenta, z_values, steps_done_total)
line = ax[1].add_collection(lc)
fig.colorbar(line, ax=ax[1])
ax[1].set_xlim(momenta.min() - paddingx, momenta.max() + paddingx)
ax[1].set_ylim(z_values.min() - paddingy, z_values.max() + paddingy)
ax[1].legend()

os.chdir(cfg_dir)
plt.savefig("plot.png", bbox_inches="tight")
