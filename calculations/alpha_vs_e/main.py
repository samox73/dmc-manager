from calculations.utils import assure_input_correct, checkpoint_func, save_func
from manager.json_parser import file_to_json
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
for alpha, mu, max_step, e_estimate in zip(
    alphas, mus, max_steps, energy_estimates
):
    print(f"\t{alpha:.4f}\t\t{mu:.4f}")
    # build the patch object
    patch = {
        "/Configuration/alpha": alpha,
        "/Configuration/momentum": momentum,
        "/Measurements/energy/estimate": e_estimate,
        "/Configuration/mu": mu,
        "/Simulation/max_steps": max_step,
        "/Simulation/max_time": 999_999_999,
    }
    # generate and save the config in an array
    config = easy_config.generate(**patch)
    configs.append(config)

executor = run_executor().configs(configs).run_dir(run_dir).store(store)

if assure_input_correct("Clear all data?"):
    executor.initialize(clear=True)
else:
    executor.initialize(clear=False)

executor.set_index("input.Configuration.momentum")
executor.run("mpirun -c 14 dmc")
