import os
from pathlib import Path
from manager.json_parser import fft_to_json, file_to_json
import sys
from bson.binary import Binary
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection


def save_func(**kwargs):
    fft_raw = fft_to_json()
    fft = {
        "taus": fft_raw["tau"],
        "G0_t": fft_raw["G0_t"],
        "S_higher_t": fft_raw["S_higher_t"],
        "G_w": fft_raw["G_w"],
        "G_t": fft_raw["G_t"],
    }
    run_properties = file_to_json("run_properties.json")
    input_json = file_to_json("input.json")
    checkpoints = []
    for file in Path(os.getcwd()).glob("thread*"):
        checkpoints.append(Binary(file.read_bytes()))
    return {
        "input": input_json,
        "run_properties": run_properties,
        "fft": fft,
        "checkpoints": checkpoints,
        "tags": kwargs["tags"] if kwargs.keys().__contains__("tags") else {},
    }


def assure_input_correct(question):
    valid_trues = ["y", "yes"]
    sys.stdout.write(question + " [y/n] ")
    choice = input().lower()
    return choice in valid_trues


def build_color_linecollection(x, y, w):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(w.min(), w.max())
    lc = LineCollection(segments, cmap="viridis", norm=norm)
    lc.set_array(w)
    lc.set_linewidth(2)
    return lc
