from calculations.utils import assure_input_correct, save_func
from manager.run_executor import run_executor
from manager.factory.easy_config import *
from parameters import *


# specify all arguments
easy_config = easy_config()
easy_config.get_default_input(cfg_template_path)

# iterate over all iterable arguments
configs = []
print(f"\talpha\tmu")
print(f"\t--------------")
for momentum, mu, max_step in zip(momenta, mus, max_steps):
    # build the patch object
    print(f"\t{alpha:.2f}\t{mu:.2f}")
    patch = {
        "/Configuration/alpha": alpha,
        "/Configuration/momentum": momentum,
        "/Configuration/mu": mu,
        "/Simulation/max_steps": max_step,
        "/Simulation/max_time": 999_999_999,
    }
    # generate and save the config in an array
    config = easy_config.generate(**patch)
    configs.append(config)

clear = False
if clear and not assure_input_correct("Clearing all DB documents, continue?"):
    print("Aborting...")
    exit(0)

executor = run_executor().configs(configs).run_dir(run_dir).store(store)
executor.initialize(clear=clear)
if clear:
    c = store.collection.delete_many({"tags.project": project_name})
    print(f"Deleted {c.deleted_count} documents from the store")
    executor.run("mpirun -c 12 dmc")


executor.save(function=save_func, tags={"project": project_name})
