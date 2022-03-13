from pathlib import Path
import shutil
from calculations.utils import assure_input_correct, save_func
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
run_dir = f"{cfg_dir}/rerun"
shutil.rmtree(run_dir, ignore_errors=True)
os.mkdir(run_dir)
os.chdir(run_dir)
for doc in docs:
    input = doc["input"]
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
    for f in Path(run_dir).glob("*"):
        os.remove(f)
