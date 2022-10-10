from calculations.utils import assure_input_correct, checkpoint_func, save_func
from manager.json_parser import file_to_json
from manager.run_executor import run_executor
from manager.factory.easy_config import *
from parameters_1 import *


def index_func():
    input_json = file_to_json("input.json")
    index = {"input.Configuration.momentum": input_json["Configuration"]["momentum"]}
    return index


# specify all arguments
easy_config = easy_config()
easy_config.get_default_input(cfg_template_path)

# iterate over all iterable arguments
configs = []
print(f"\tidx\tmomentum\tmu\tsteps")
for i, momentum, mu, max_step, e_estimate in zip(
    range(len(momenta)), momenta, mus, max_steps, energy_estimates
):
    print(f"\t{i}\t{momentum:.4f}\t\t{mu:.4f}\t{max_step}")
    # build the patch object
    patch = {
        "/Configuration/alpha": alpha,
        "/Configuration/momentum": momentum,
        "/Measurements/energy/estimate": e_estimate,
        "/Measurements/energy/delta": e_delta,
        "/Configuration/mu": mu,
        "/Simulation/max_steps": max_step,
        "/Simulation/max_time": 999_999_999,
        "/RNG/seed": 8221265147609980501 + i * 123456,
    }
    # generate and save the config in an array
    config = easy_config.generate(**patch)
    configs.append(config)

executor = run_executor().configs(configs).run_dir(runs_dir).store(store)

if assure_input_correct("Clear all data?"):
    executor.initialize(clear=True)
else:
    executor.initialize(clear=False)


if clear_db:
    c = store.collection.delete_many({"tags.project": project_name})
    print(f"Deleted {c.deleted_count} documents from the store")

executor.set_index("input.Configuration.momentum")
executor.run("mpirun -c 14 dmc", index_path=["Configuration", "momentum"])
