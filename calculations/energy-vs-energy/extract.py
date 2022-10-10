import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from manager.json_parser import file_to_json

jk_data = file_to_json("run/out_jackknife.json")
e_in = jk_data["E"]["inputs"]
e_out = jk_data["E"]["means"]
e_err = jk_data["E"]["stderrs"]

plt.plot(e_in, e_in, "k")
plt.errorbar(e_in, e_out, yerr=e_err, marker="o")
plt.savefig("plot.png")

df = pd.DataFrame({"e_in": e_in, "e_out": e_out, "e_err": e_err})
df.to_csv("energy-vs-energy.csv", index=False, float_format="%.5f")
