from cProfile import label
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from calculations.utils import build_color_linecollection
from manager.analyzer import E1, E2, exp_model, fit_exp
from manager.json_parser import file_to_json


def analyze_dir(dir, z_estimate):
    run_dir = f"/home/samox/computing/dmcmanager/calculations/greens_function_fit/{dir}"
    os.chdir(run_dir)
    properties = file_to_json("out_run_properties.json")
    mu = properties["mu"]
    fft_data = file_to_json("out_fft.json")
    taus = np.array(fft_data["tau"])
    G_t = np.array(fft_data["G_t"])
    z, e = fit_exp(
        taus,
        G_t,
        properties,
        begin=15,
        z_estimate=z_estimate,
        e_estimate=file_to_json("input.json")["Measurements"]["energy"]["estimate"],
    )
    print(f"z = {z}")
    print(f"e = {e}")
    os.chdir("..")
    return taus, G_t, z, e, mu


# Setup
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

taus, G_t, z, e, mu = analyze_dir("run_alpha-1", 0.59)
fit = exp_model(taus, z, e - mu)
ax[0].plot(taus, G_t, label="$G_t$")
ax[0].plot(taus, fit, linestyle="dashed", color="#343400", label="fit")
ax[0].legend()
pd.DataFrame(
    {
        "taus": taus,
        "g": G_t,
        "fit": exp_model(taus, z, e - mu),
    }
).to_csv("greens-function-fit-alpha-1.csv", index=False, float_format="%.5f")


taus, G_t, z, e, mu = analyze_dir("run_alpha-5", 0.03)
fit = exp_model(taus, z, e - mu)
ax[1].plot(taus, G_t, label="$G_t$")
ax[1].plot(taus, fit, linestyle="dashed", color="#343400", label="fit")
ax[1].legend()
pd.DataFrame(
    {
        "taus": taus,
        "g": G_t,
        "fit": exp_model(taus, z, e - mu),
    }
).to_csv("greens-function-fit-alpha-5.csv", index=False, float_format="%.5f")

plt.savefig("plot.png", bbox_inches="tight")
