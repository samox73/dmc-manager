from input_config import *
import numpy as np

kwargs = {
    "/Configuration/alpha_": "2"
}

factory = multi_alpha_config()

json_string = factory.alphas(np.linspace(1, 2, 5)).get_input(0)

with open("input.json", "w") as input_file:
    input_file.write(json_string)
