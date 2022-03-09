import json
import os
import sys
from types import SimpleNamespace
import jsonpatch
import importlib.resources as pkg_resources


class input_config:

    def get_default_input(self, cfg_path):
        modname = globals()['__name__']
        module = sys.modules[modname]
        print(os.getcwd())
        with open(cfg_path, "r") as file:
            text = file.read()
            return json.loads(text, object_hook=lambda d: SimpleNamespace(**d))

    # def generate(self, cfg_path, **kwargs):
    #     input = self.get_default_input(cfg_path)
    #     patch = []
    #     for key, value in kwargs.items():
    #         patch.append({"op": "replace", "path": key, "value": value})
    #     jsonpatch.apply_patch(input, patch, in_place=True)
    #     return json.dumps(input, indent=2, default=lambda o: o.__dict__, sort_keys=True)
