from cycler import cycler
import matplotlib.pyplot as plt

colors = ["#24D671", "#B5574C", "#587FFC", "#383966", "#6931EB", "#4A0314", "#B4BD62"]

custom_cycler = cycler(color=colors)


def setup_matplotlib():
    plt.rc("axes", prop_cycle=custom_cycler)
