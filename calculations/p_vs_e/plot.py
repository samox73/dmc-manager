import os
from manager.analyzer import E1, E2, fit_exp
from parameters import *

# ============= RETRIEVAL =============

filter = {"run_properties.alpha": alpha, "tags.project": project_name}
results = store.collection.find(filter)
N = store.collection.count_documents(filter)
print(f"retrieved {N} documents with filter {filter}")

fig, ax = plt.subplots(1, 3, figsize=(20, 6))

z_estimates = np.linspace(0.6, 0, N)
energies = []
momenta = []
z_values = []
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
    energies.append(e)
    z_values.append(z)
    ax[2].plot(taus, G_t)

momenta_fine = np.linspace(0, 1.4, 1000)
ax[0].plot(momenta, energies, label=f"E")
ax[0].plot(momenta_fine, E1(momenta_fine, alpha), linestyle="--", label="E1")
ax[0].plot(momenta_fine, E2(momenta_fine, alpha), linestyle="--", label="E2")
ax[0].legend()
ax[1].plot(momenta, z_values, label=f"Z")
ax[1].legend()
os.chdir(cfg_dir)
plt.savefig("plot.png", bbox_inches="tight")
