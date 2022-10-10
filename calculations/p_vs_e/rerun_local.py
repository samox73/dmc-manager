import subprocess, os, datetime
from manager.json_parser import string_to_file
from parameters import *
from manager.factory.easy_config import *

config = config()

cmd = "mpirun -c 14 dmc"
for root, dirs, files in os.walk(runs_dir):
    for dir in dirs:
        # specify all arguments
        os.chdir(f"{os.path.join(root, dir)}")

        # patch config
        config.get_default_input("input.json")
        if config.config_["Configuration"]["momentum"] < 1:
            continue
        patch = {
            "/Simulation/max_steps": 1_000_000_000,
            "/Simulation/max_time": 999_999_999,
            "/Simulation/cycles_per_check": 10_000_000,
        }
        config = config.generate(**patch)
        string_to_file(config, "input.json")

        print(f"Starting simulation for {dir}")
        with open("log.txt", "w") as log:
            subprocess.run(cmd.split(), stderr=subprocess.STDOUT, stdout=log)

subprocess.run(['/home/samox/computing/bin/push_to_app', 'p-vs-e', f'Job finished on arceus@{datetime.datetime.now()}'])
