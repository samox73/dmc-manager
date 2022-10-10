from calculations.utils import assure_input_correct
from manager.json_parser import file_to_json
from manager.run_executor import run_executor
from manager.factory.easy_config import *
from parameters_3 import *

# specify all arguments
easy_config = easy_config()
easy_config.get_default_input(cfg_template_path)

# iterate over all iterable arguments
configs = []
print(f"\tidx\tmax order\tmu\tsteps")
for i, max_order, max_step, energy_estimate, mu in zip(
    range(len(max_orders)), max_orders, max_steps, energy_estimates, mus
):
    print(f"\t{i}\t{max_order:.0f}\t\t{mu:.3f}\t{max_step:.0f}")
    # build the patch object
    patch = {
        "/Configuration/alpha": alpha,
        "/Configuration/momentum": momentum,
        "/Configuration/mu": mu,
        "/Configuration/max_order": max_order,
        "/Measurements/energy/interpolation_size": 10000,
        "/Measurements/energy/estimate": energy_estimate,
        "/Measurements/energy/delta": energy_delta,
        "/Measurements/diagram_statistics/diagram_order/end": max_order + 100,
        "/Measurements/diagram_statistics/diagram_order/size": max_order + 101,
        "/Simulation/max_steps": max_step,
        "/Simulation/max_time": 999_999_999,
        "/RNG/seed": 8221265147609980501,
    }
    # generate and save the config in an array
    config = easy_config.generate(**patch)
    configs.append(config)

executor = run_executor().configs(configs).run_dir(runs_dir)

if assure_input_correct("Clear all data?"):
    executor.initialize(clear=True)
else:
    executor.initialize(clear=False)

executor.run("mpirun -c 14 dmc")
