import json
import subprocess
import os
import shutil

from scipy.fft import fft

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

    def run(self, cmds="dmc"):
        for run_dir in self.run_dirs_:
            os.chdir(f"{self.runs_dir_}/{run_dir}")
            subprocess.run(cmds.split())

    def save(self, function):
        for run_dir in self.run_dirs_:
            os.chdir(f"{self.runs_dir_}/{run_dir}")
            items = function()
            self.store_.add(items)
