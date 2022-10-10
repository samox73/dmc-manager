from cProfile import label
import os
from calculations.utils import build_color_linecollection
from manager.analyzer import E1, E2, fit_exp
from manager.json_parser import file_to_json
from parameters_1 import *
import pandas as pd

# Setup
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
energies = []
energy_errs = []
zs = []
z_errs = []
momenta = []
momenta_fine = np.linspace(0, 1.4, 1000)

for root, dirs, files in os.walk(runs_dir):
    for dir in dirs:
        if "bak" in dir:
            continue
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
            momenta.append(properties["momentum"])
        except Exception as e:
            print(e)

momenta = np.array(momenta)
energies = np.array(energies)
energy_errs = np.array(energy_errs)
zs = np.array(zs)
z_errs = np.array(z_errs)
# e1 = E1(momenta_fine, alpha)
# e2 = E2(momenta_fine, alpha)

# sort arrays
p = momenta.argsort()
momenta = momenta[p]
energies = energies[p]
zs = zs[p]

print(f"momenta  = {np.array2string(momenta, separator=', ')}")
print(f"energies = {np.array2string(energies, separator=', ')}")

print(f"\tidx\tmomentum\tenergy\t\tz")
for i, momentum, energy, z in zip(range(len(momenta)), momenta, energies, zs):
    print(f"\t{i}\t{momentum:.3f}\t\t{energy:.4f}\t\t{z:.4f}")

# ax[0].plot(momenta_fine, e1, linestyle="dashdot", color="#343400", label="E1")
# ax[0].plot( momenta_fine, e2, linestyle="dashed", color="#343400", label="E2")

paddingx = 0.1
paddingy = 0.05

ax[0].errorbar(momenta, energies, yerr=energy_errs, marker=".")
print(momenta[np.where(energies > energies[0] + 1)[0][0]])
ax[0].plot(momenta, (energies[0] + 1) * np.ones(len(momenta)), "k")
ax[0].set_xlim(momenta.min() - paddingx, momenta.max() + paddingx)
ax[0].set_ylim(energies.min() - paddingy, energies.max() + paddingy)
ax[0].grid()

ax[1].errorbar(momenta, zs, yerr=z_errs, marker=".")
ax[1].set_xlim(momenta.min() - paddingx, momenta.max() + paddingx)
ax[1].set_ylim(zs.min() - paddingy, zs.max() + paddingy)

os.chdir(cfg_dir)
plt.savefig(f"alpha-{alpha}-direct.png", bbox_inches="tight")

pd.DataFrame(
    {
        "p": momenta,
        "e": energies,
        "z": zs,
        "e_err": energy_errs,
        "z_err": z_errs,
    }
).to_csv(f"momentum-vs-energy-alpha-{alpha}.csv", index=False, float_format="%.5f")

# pd.DataFrame(
#     {
#         "p": momenta_fine,
#         "e1": e1,
#         "e2": e2,
#     }
# ).to_csv("momentum-vs-energy-analytic.csv", index=False, float_format="%.5f")
