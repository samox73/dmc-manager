from cProfile import label
import os
import matplotlib.pyplot as plt
from calculations.utils import build_color_linecollection
from manager.analyzer import E1, E2, fit_exp
from manager.json_parser import file_to_json
from parameters import *
import pandas as pd

# Setup
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
energies = []
energy_errs = []
zs = []
z_errs = []
alphas = []
alphas_fine = np.linspace(0, 6, 1000)

for root, dirs, files in os.walk(run_dir):
    for dir in dirs:
        print(f"analyzing dir '{dir}'")
        os.chdir(f"{os.path.join(root, dir)}")
        try:
            data = file_to_json("out_jackknife.json")
            properties = file_to_json("out_run_properties.json")
            if data["E"]["estimate"]["value"] is None:
                continue
            energies.append(data["E"]["estimate"]["value"])
            energy_errs.append(data["E"]["estimate"]["error"])
            zs.append(data["Z"]["estimate"]["value"])
            z_errs.append(data["Z"]["estimate"]["error"])
            alphas.append(properties["alpha"])
        except Exception as e:
            print(e)

alphas = np.array(alphas)
energies = np.array(energies)
energy_errs = np.array(energy_errs)
zs = np.array(zs)
z_errs = np.array(z_errs)
e1 = E1(momentum, alphas_fine)
e2 = E2(momentum, alphas_fine)

# sort arrays
p = alphas.argsort()
alphas = alphas[p]
energies = energies[p]
zs = zs[p]

print(f"\talpha\tenergy")
for alpha, energy in zip(alphas, energies):
    print(f"\t{alpha:.3f}\t{energy:.4f}")

ax[0].plot(
    alphas_fine,
    e1,
    linestyle="dashdot",
    color="#343400",
    label="E1",
)
ax[0].plot(
    alphas_fine,
    e2,
    linestyle="dashed",
    color="#343400",
    label="E2",
)

paddingx = 0.1
paddingy = 0.05

ax[0].plot(alphas, list(energies), "-o")
ax[0].set_xlim(alphas.min() - paddingx, alphas.max() + paddingx)
ax[0].set_ylim(energies.min() - paddingy, energies.max() + paddingy)
ax[0].legend()

ax[1].plot(alphas, zs, "-o")
ax[1].set_xlim(alphas.min() - paddingx, alphas.max() + paddingx)
ax[1].set_ylim(zs.min() - paddingy, zs.max() + paddingy)
ax[1].legend()

os.chdir(cfg_dir)
plt.savefig("plot.png", bbox_inches="tight")

pd.DataFrame(
    {
        "alphas": alphas,
        "e": energies,
        "z": zs,
        "e_err": energy_errs,
        "z_err": z_errs,
    }
).to_csv("alpha-vs-energy.csv", index=False, float_format="%.5f")

pd.DataFrame(
    {
        "alphas": alphas_fine,
        "e1": e1,
        "e2": e2,
    }
).to_csv("alpha-vs-energy-analytic.csv", index=False, float_format="%.5f")
