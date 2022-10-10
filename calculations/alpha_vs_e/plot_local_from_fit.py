from cProfile import label
import os
import matplotlib.pyplot as plt
from calculations.utils import build_color_linecollection
from manager.analyzer import E1, E2, fit_exp
from manager.json_parser import file_to_json
from parameters import *

# Setup
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
energies = []
energy_stderrs = []
zs = []
z_stderrs = []
alphas = []
alphas_fine = np.linspace(0, 10, 1000)

for root, dirs, files in os.walk(run_dir):
    for dir in dirs:
        print(f"analyzing dir '{dir}'")
        os.chdir(f"{os.path.join(root, dir)}")
        try:
            properties = file_to_json("out_run_properties.json")
            fft_data = file_to_json("out_fft.json")
            taus = np.array(fft_data["tau"])
            G_t = np.array(fft_data["G_t"])
            z, e = fit_exp(
                taus,
                G_t,
                properties,
                z_estimate=0.5,
                e_estimate=file_to_json("input.json")["Measurements"]["energy"][
                    "estimate"
                ],
            )
            energies.append(e)
            zs.append(z)
            alphas.append(properties["alpha"])
        except Exception as e:
            print(e)

alphas = np.array(alphas)
energies = np.array(energies)
zs = np.array(zs)

# sort arrays
p = alphas.argsort()
alphas = alphas[p]
energies = energies[p]
zs = zs[p]

print(f"\talpha\tenergy")
for alpha, energy in zip(alphas, energies):
    print(f"\t{alpha:.3f}\t{energy:.4f}")

print(f"alphas   = {np.array2string(alphas, separator=', ')}")
print(f"energies = {np.array2string(energies, separator=', ')}")

ax[0].plot(
    alphas_fine,
    E1(momentum, alphas_fine),
    linestyle="dashdot",
    color="#343400",
    label="E1",
)
ax[0].plot(
    alphas_fine,
    E2(momentum, alphas_fine),
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
