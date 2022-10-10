import os
import matplotlib.pyplot as plt
from calculations.utils import build_color_linecollection
from manager.analyzer import E1, E2, fit_exp
from manager.json_parser import file_to_json
from parameters_1 import *
import pandas as pd

# Setup
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
energies = []
energy_stderrs = []
zs = []
z_stderrs = []
momenta = []
momenta_fine = np.linspace(0, 5, 1000)

for root, dirs, files in os.walk(runs_dir):
    for dir in dirs:
        print(f"analyzing dir '{dir}'")
        os.chdir(f"{os.path.join(root, dir)}")
        try:
            properties = file_to_json("out_run_properties.json")
            fft_data = file_to_json("out_fft.json")
            taus = np.array(fft_data["tau"])
            G_t = np.array(fft_data["G_t"])
            e_est = file_to_json("input.json")["Measurements"]["energy"]["estimate"]
            z, e = fit_exp(
                taus,
                G_t,
                properties,
                z_estimate=0.5,
                e_estimate=e_est,
            )
            energies.append(e)
            zs.append(z)
            momenta.append(properties["momentum"])
        except Exception as e:
            print(e)

momenta = np.array(momenta)
energies = np.array(energies)
# energies = energies - energies[0]
zs = np.array(zs)

# sort arrays
p = momenta.argsort()
momenta = momenta[p]
energies = energies[p]
zs = zs[p]

print(f"\tmomentum\tenergy\tz")
for momentum, energy, z in zip(momenta, energies, zs):
    print(f"\t{momentum:.3f}\t{energy:.4f}\t{z:.4f}")

print(f"momenta  = {np.array2string(momenta, separator=', ')}")
print(f"energies = {np.array2string(energies, separator=', ')}")
print(f"zs       = {np.array2string(zs, separator=', ')}")

paddingx = 0.1
paddingy = 0.05

ax[0].plot(momenta, list(energies), "-o")
ax[0].plot(momenta, (energies[0] + 1) * np.ones(len(momenta)), "k")
ax[0].set_xlim(momenta.min() - paddingx, momenta.max() + paddingx)
ax[0].set_ylim(energies.min() - paddingy, energies.max() + paddingy)
ax[0].legend()
ax[0].set_title(f"alpha = {alpha}")

ax[1].plot(momenta, zs, "-o")
ax[1].set_xlim(momenta.min() - paddingx, momenta.max() + paddingx)
ax[1].set_ylim(zs.min() - paddingy, zs.max() + paddingy)
ax[1].legend()
ax[1].set_title(f"alpha = {alpha}")

os.chdir(cfg_dir)
plt.savefig(f"alpha-{alpha}.png", bbox_inches="tight")

