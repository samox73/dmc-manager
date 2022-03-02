import json
import subprocess
import os
import shutil

from scipy.fft import fft
from manager.json_parser import fft_to_json, run_properties_to_json

from manager.store import store


class run_executor:
    run_dirs_ = []

    def configs(self, configs):
        self.configs_ = configs
        return self

    def store(self, store):
        self.store_ = store
        return self

    def run_dir(self, run_dir):
        self.runs_dir_ = run_dir
        return self

    def clear(self):
        shutil.rmtree(self.runs_dir_, ignore_errors=True)

    def initialize(self, reset=False):
        self.run_dirs_.clear()
        if reset:
            self.clear()
        try:
            os.mkdir(self.runs_dir_)
        except Exception as error:
            print(error)
        os.chdir(self.runs_dir_)

        for config, params, index in self.configs_:
            run_dir = f"run_{index}"
            self.run_dirs_.append(run_dir)
            try:
                os.mkdir(run_dir)
                os.chdir(run_dir)
                with open("input.json", "w") as input_file:
                    input_file.write(config)
                print(params)
            except Exception as e:
                print(f"Got error: {e}")
            os.chdir(self.runs_dir_)

    def run(self, executable="self_energy_dmc", filename="input.json"):
        for run_dir in self.run_dirs_:
            os.chdir(f"{self.runs_dir_}/{run_dir}")
            print(f"Starting simulation in {run_dir}")
            subprocess.run([executable, filename])

    def save(self):
        for run_dir in self.run_dirs_:
            os.chdir(f"{self.runs_dir_}/{run_dir}")
            print(f"Saving {run_dir}")
            fft_raw = fft_to_json()
            fft = {
                "taus": fft_raw["tau"],
                "G0_t": fft_raw["G0_t"],
                "S_higher_t": fft_raw["S_higher_t"],
                "G_w": fft_raw["G_w"],
                "G_t": fft_raw["G_t"],
            }
            run_properties = run_properties_to_json()
            self.store_.add(run_properties, fft)
