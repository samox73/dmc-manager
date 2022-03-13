import json
from re import sub
import subprocess
import os
import shutil
from functools import reduce
import operator

from manager.json_parser import file_to_json


class run_executor:
    run_dirs_ = []
    generated_config_filename_ = "input.json"

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

    def initialize(self, clear=False):
        self.run_dirs_.clear()
        if clear:
            self.clear()
        try:
            os.mkdir(self.runs_dir_)
        except Exception as error:
            print(error)
        os.chdir(self.runs_dir_)

        index = 0
        for config in self.configs_:
            run_dir = f"run_{index}"
            index += 1
            self.run_dirs_.append(run_dir)
            try:
                os.mkdir(run_dir)
                os.chdir(run_dir)
                with open(self.generated_config_filename_, "w") as input_file:
                    input_file.write(config)
            except Exception as e:
                print(f"Got error: {e}")
            os.chdir(self.runs_dir_)

    def load_checkpoints(self, index_path=None):
        cfg = file_to_json(self.generated_config_filename_)
        # access dict by array of keys
        value = reduce(operator.getitem, index_path, cfg)
        object = self.store_.collection.find_one(
            {self.index_: value, "checkpoints": {"$exists": True}}
        )
        if object is None:
            return
        print(f"Found checkpoints in database (index: {self.index_}={value})")
        checkpoints = object["checkpoints"]
        for idx, checkpoint in zip(range(len(checkpoints)), checkpoints):
            with open(f"thread_{idx}", "wb") as f:
                f.write(checkpoint)

    def run(self, cmds="dmc", index_path=None):
        for run_dir in self.run_dirs_:
            os.chdir(f"{self.runs_dir_}/{run_dir}")
            print(f"Starting simulation for {run_dir}")
            if self.index_ is not None and index_path is not None:
                self.load_checkpoints(index_path)
            with open("log.txt", "w") as log:
                subprocess.run(cmds.split(), stderr=subprocess.STDOUT, stdout=log)

    def set_index(self, index):
        self.store_.collection.create_index(index)
        self.index_ = index

    def save(self, index_function, object_function, **kwargs):
        """Saves the outputs of the supplied function to the MongoDB

        Args:
            index_function: needs to return an index
            object_function: needs to return the object to be saved
        """
        for run_dir in self.run_dirs_:
            os.chdir(f"{self.runs_dir_}/{run_dir}")
            index = index_function()
            items = object_function(**kwargs)
            self.store_.collection.replace_one(index, items, upsert=True)
