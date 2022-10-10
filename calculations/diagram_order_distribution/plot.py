import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from manager.json_parser import file_to_json

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

stats = file_to_json("run_alpha-1/out_diag_stats.json")["diagram_order"]
grid = np.array(stats["grid"])
hist = np.array(stats["histogram"])
idx = np.where(hist == 0)[0][0]
grid = grid[:idx]
hist = hist[:idx]
print(grid[-1])
ax[0].bar(grid, hist, width=grid[1] - grid[0])
df = pd.DataFrame({"order": grid, "density": hist})
df.to_csv("diagram-order-density-alpha-1.csv", index=False, float_format="%.5f")

stats = file_to_json("run_alpha-5/out_diag_stats.json")["diagram_order"]
grid = np.array(stats["grid"])
hist = np.array(stats["histogram"])
idx = np.where(hist == 0)[0][0]
grid = grid[:idx]
hist = hist[:idx]
print(grid[-1])
ax[1].bar(grid, hist, width=grid[1] - grid[0])
df = pd.DataFrame({"order": grid, "density": hist})
df.to_csv("diagram-order-density-alpha-5.csv", index=False, float_format="%.5f")

fig.savefig("plot.png")
