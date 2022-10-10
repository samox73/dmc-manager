import json
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
    fft = file_to_json("out_fft.json")
    run_properties = file_to_json("out_run_properties.json")
    input_json = file_to_json("input.json")
    return {
        "input": input_json,
        "run_properties": run_properties,
        "jackknife": {
            "E": {},
        },
        "tags": kwargs["tags"] if kwargs.keys().__contains__("tags") else {},
    }


def checkpoint_func():
    checkpoints = []
    for file in Path(os.getcwd()).glob("thread*"):
        checkpoints.append(Binary(file.read_bytes()))
    return checkpoints


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
