import json
import jsonpatch

j = {
    "Configuration": {
        "alpha": 1,
        "max_tau": 20
    }
}

jsonpatch.apply_patch(
    j, [{"op": "replace", "path": "/Configuration/alpha", "value": 2}])
