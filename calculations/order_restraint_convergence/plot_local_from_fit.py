import os
import matplotlib.pyplot as plt
from manager.analyzer import fit_exp
from manager.json_parser import file_to_json
from parameters_1 import *
import pandas as pd

# Setup
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
energies_fit = []
zs_fit = []
energies = []
energy_errs = []
zs = []
z_errs = []
max_orders = []


def extract_fit():
    properties = file_to_json("out_run_properties.json")
    fft_data = file_to_json("out_fft.json")
    taus = np.array(fft_data["tau"])
    G_t = np.array(fft_data["G_t"])
    energy_estimate = file_to_json("input.json")["Measurements"]["energy"]["estimate"]
    z_estimate = z_estimates[np.where(energy_estimates == energy_estimate)[0][0]]
    z, e = fit_exp(
        taus,
        G_t,
        properties,
        z_estimate=z_estimate,
        e_estimate=energy_estimate,
    )
    return e, z, properties["max_order"]


def extract_estimates():
    data = file_to_json("out_jackknife.json")
    properties = file_to_json("out_run_properties.json")
    e = data["E"]["estimate"]["value"]
    e_err = data["E"]["estimate"]["error"]
    z = data["Z"]["estimate"]["value"]
    z_err = data["Z"]["estimate"]["error"]
    return e, e_err, z, z_err


for root, dirs, files in os.walk(runs_dir):
    for dir in dirs:
        print(f"analyzing dir '{dir}'")
        os.chdir(f"{os.path.join(root, dir)}")
        try:
            e, z, max_order = extract_fit()
            energies_fit.append(e)
            zs_fit.append(z)
            max_orders.append(max_order)

            e, e_err, z, z_err = extract_estimates()
            energies.append(e)
            energy_errs.append(e_err)
            zs.append(z)
            z_errs.append(z_err)
        except Exception as e:
            print(e)

max_orders = np.array(max_orders)
energies_fit = np.array(energies_fit)
zs_fit = np.array(zs_fit)
energies = np.array(energies)
energy_errs = np.array(energy_errs)
zs = np.array(zs)
z_errs = np.array(z_errs)

print(f"\tmax_order\tenergy\tz")
for max_order, energy, z in zip(max_orders, energies_fit, zs_fit):
    print(f"\t{max_order:.3f}\t{energy:.4f}\t{z:.4f}")

print(f"max_orders      = {np.array2string(max_orders, separator=', ')}")
print(f"energies (fit)  = {np.array2string(energies_fit, separator=', ')}")
print(f"zs (fit)        = {np.array2string(zs_fit, separator=', ')}")
print(f"energies        = {np.array2string(energies, separator=', ')}")
print(f"zs              = {np.array2string(zs, separator=', ')}")

paddingx = 0.1
paddingy = 0.05

ax[0].plot(max_orders, energies_fit, "-o", label="energy fit")
ax[0].plot(max_orders, energies, "-o", label="energy est")
ax[0].set_xlim(max_orders.min() - paddingx, max_orders.max() + paddingx)
ax[0].set_ylim(energies_fit.min() - paddingy, energies_fit.max() + paddingy)
ax[0].legend()
ax[0].set_title(f"alpha = {alpha}")

ax[1].plot(max_orders, zs_fit, "-o", label="z fit")
ax[1].plot(max_orders, zs, "-o", label="z est")
ax[1].set_xlim(max_orders.min() - paddingx, max_orders.max() + paddingx)
ax[1].set_ylim(zs_fit.min() - paddingy, zs_fit.max() + paddingy)
ax[1].legend()
ax[1].set_title(f"alpha = {alpha}")

os.chdir(cfg_dir)
plt.savefig(f"alpha-{alpha}.png", bbox_inches="tight")

pd.DataFrame(
    {
        "orders": max_orders,
        "e": energies_fit,
        "z": zs_fit,
    }
).to_csv(f"max-order-alpha-{alpha}.csv", index=False, float_format="%.5f")
