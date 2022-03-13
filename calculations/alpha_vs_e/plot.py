import imp
import os
from manager.analyzer import *
from parameters import *
from calculations.colors import setup_matplotlib

setup_matplotlib()

# ============= RETRIEVAL =============
filter = {
    "run_properties.momentum": momentum,
    "tags.project": project_name,
    "run_properties.steps_done_total": {"$gt": 2000000000},
}
results = store.collection.find(filter)
N = store.collection.count_documents(filter)
print(f"retrieved {N} documents with filter {filter}")

fig, ax = plt.subplots(1, 3, figsize=(20, 6))

z_estimates = np.linspace(0.6, 0, N)
energies = []
alphas = []
z_values = []
print(f"\talpha\t\tE\t\tZ")
print(f"\t----------------------------------------")
for z_estimate, result in zip(z_estimates, results):
    fft = result["fft"]
    taus = np.array(fft["taus"])
    G_t = np.array(fft["G_t"])
    properties = result["run_properties"]
    alpha = properties["alpha"]
    z, e = fit_exp(
        taus,
        G_t,
        properties,
        z_estimate=z_estimate,
        e_estimate=properties["mu"],
    )
    print(f"\t{alpha:.4f}\t\t{e:.4f}\t\t{z:.4f}")
    alphas.append(alpha)
    energies.append(e)
    z_values.append(z)
    ax[2].plot(taus, G_t)

p = np.array(alphas).argsort()
alphas = np.array(alphas)[p]
energies = np.array(energies)[p]
z_values = np.array(z_values)[p]

alphas_fine = np.linspace(0, 5.999, N)
alphas_short = np.linspace(0, 1, N)
ax[0].plot(alphas, energies, lw=1)
ax[0].plot(alphas_fine, E1(momentum, alphas_fine), lw=1, linestyle="--", label="E1")
ax[0].plot(alphas_fine, E2(momentum, alphas_fine), lw=1, linestyle="--", label="E2")
ax[0].scatter(alphas, energies, s=4, label=f"E")
ax[0].legend()
ax[1].plot(alphas, z_values, label=f"Z")
ax[1].plot(alphas_short, Z1(alphas_short), linestyle="--", label="Z1")
ax[1].legend()
os.chdir(cfg_dir)
plt.savefig("plot.png", bbox_inches="tight")
