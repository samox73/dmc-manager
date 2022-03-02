from manager import json_parser
import matplotlib.pyplot as plt

j = json_parser.fft_to_json("fft.dat")
print(j.keys())

plt.plot(j["tau"], j["G0_t"])
plt.show()
