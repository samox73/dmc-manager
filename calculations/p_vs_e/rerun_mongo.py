"""
This file scans the supplied mongo collection, fetches documents (previous runs) that match
a filter and then runs a simulation for each of these runs again.
"""
from pathlib import Path
import shutil
from calculations.utils import save_func
from manager.json_parser import file_to_json
from manager.factory.easy_config import *
from parameters import *
import subprocess


def index_func():
    input_json = file_to_json("input.json")
    index = {"input.Configuration.momentum": input_json["Configuration"]["momentum"]}
    return index


filter = {"input.Configuration.momentum": {"$gt": 1.2}}
docs = store.collection.find(filter)
N = store.collection.count_documents(filter)
print(f"Found {N} documents that match the filter {filter}")
runs_dir = f"{cfg_dir}/rerun"
shutil.rmtree(runs_dir, ignore_errors=True)
os.mkdir(runs_dir)
os.chdir(runs_dir)

# fetch and story the found results from the database (the type of
# `docs` is not an array but a mongo pointer so we need to fetch all
# the results and save them in an array)
documents = []
for doc in docs:
    documents.append(doc.copy())

# iterate over the results and perform a simulation for each
for doc, i in zip(documents, np.arange(0, len(documents))):
    input = doc["input"]
    steps_total = doc["run_properties"]["steps_done_total"]
    # input["Simulation"]["max_steps"] = 2_000_000_000
    input["Simulation"]["warmup_steps"] = 0

    print(f"=== {i} / {len(documents) - 1} ===")
    print(f"Steps total = {steps_total}")

    with open("input.json", "w") as cfg:
        json.dump(input, cfg, indent=2)
    checkpoints = doc["checkpoints"]
    for idx, checkpoint in zip(range(len(checkpoints)), checkpoints):
        with open(f"thread_{idx}", "wb") as f:
            f.write(checkpoint)
    subprocess.run("mpirun -c 14 dmc".split())
    index = index_func()
    items = save_func(tags={"project": project_name})
    store.collection.replace_one(index, items)
    for f in Path(runs_dir).glob("*"):
        os.remove(f)
