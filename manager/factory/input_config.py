import json
import jsonpatch


class input_config:
    def get_default_input():
        return {
            "Configuration": {
                "alpha_": 1.0,
                "global_p_mod_": 0.0,
                "max_order_": 10000,
                "max_tau_": 30.0,
                "min_order_": 0,
                "mu_": -1.1,
                "order_": 0,
                "start_tau_": 1.0
            },
            "Measurements": {
                "histogram": {
                    "energy_estimate": -1.0168,
                    "is_active": True,
                    "num_bins": 2000
                }
            },
            "RNG": {
                "seed": 8267165747609980501
            },
            "Simulation": {
                "checkpoint_after_steps": 18446744073709551615,
                "checkpoint_after_time": 1.7976931348623157e+308,
                "checkpoint_callback": True,
                "cycles_per_check": 1000000,
                "load_checkpoint": False,
                "max_steps": 18446744073709551615,
                "max_time": 0.2,
                "per_cycle_callback": False,
                "per_step_callback": False,
                "skip_impossible_updates": False,
                "sort_updates": True,
                "steps_per_cycle": 5,
                "warmup_checkpoint_after_steps": 18446744073709551615,
                "warmup_checkpoint_after_time": 1.7976931348623157e+308,
                "warmup_checkpoint_callback": True,
                "warmup_per_step_callback": False,
                "warmup_steps": 18446744073709551615,
                "warmup_steps_per_cycle": 1000000,
                "warmup_time": 0.0
            },
            "Updates": {
                "add_phonon": {
                    "weight": 1.0
                },
                "change_internal_q_direction": {
                    "weight": 1.0
                },
                "change_internal_q_modulus": {
                    "weight": 1.0
                },
                "change_internal_tau": {
                    "weight": 1.0
                },
                "change_tau": {
                    "weight": 1.0
                },
                "change_topology": {
                    "weight": 1.0
                },
                "remove_phonon": {
                    "weight": 1.0
                },
                "rescale_diagram": {
                    "weight": 1.0
                }
            },
            "fft": {
                "beta": 100.0
            }
        }

    def generate(self, **kwargs):
        input = input_config.get_default_input()
        patch = []
        for key, value in kwargs.items():
            patch.append({"op": "replace", "path": key, "value": value})
        jsonpatch.apply_patch(input, patch, in_place=True)
        return json.dumps(input, indent=2)
