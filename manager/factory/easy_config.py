import json
import os
import jsonpatch


class easy_config:
    config_ = {}

    def get_default_input(self, cfg_path):
        with open(cfg_path, "r") as file:
            self.config_ = json.load(file)

    def generate(self, **kwargs):
        patch = []
        for key, value in kwargs.items():
            patch.append({"op": "replace", "path": key, "value": value})
        jsonpatch.apply_patch(self.config_, patch, in_place=True)
        return json.dumps(
            self.config_, indent=2, default=lambda o: o.__dict__, sort_keys=True
        )
