from distutils.command.config import config
from manager.factory.input_config import *
import itertools


class multi_config:
    alphas_ = [1]
    momenta_ = [0]
    max_time_ = 99_999_999_999
    max_steps_ = 99_999_999_999
    factory_ = input_config()

    def build(self, cfg_path):
        self.config_ = self.factory_.get_default_input(cfg_path)
        items = list(itertools.product(self.alphas_, self.momenta_))
        params = ["alpha", "momentum", "max_time", "max_steps"]
        self.elements_ = []
        for item in items:
            item = list(item)
            item.append(self.max_time_)
            item.append(self.max_steps_)
            self.elements_.append(dict(zip(params, item)))

    def alphas(self, a):
        self.alphas_ = a
        return self

    def max_time(self, a):
        self.max_time_ = a
        return self

    def max_steps(self, a):
        self.max_steps_ = a
        return self

    def momenta(self, p):
        self.momenta_ = p
        return self

    def get_config(self, element):
        self.config_.Configuration.alpha = element["alpha"]
        self.config_.Configuration.momentum = element["momentum"]
        self.config_.Simulation.max_time = element["max_time"]
        self.config_.Simulation.max_steps = element["max_steps"]
        return json.dumps(
            self.config_, indent=2, default=lambda o: o.__dict__, sort_keys=True
        )

    def size(self):
        return len(self.elements_)

    def __iter__(self):
        return multi_config_iterator(self)


class multi_config_iterator:
    def __init__(self, config):
        self.config_ = config
        self.index_ = 0

    def __next__(self):
        if self.index_ < self.config_.size():
            element = self.config_.elements_[self.index_]
            result = self.config_.get_config(element)
            self.index_ += 1
            return result, element, self.index_
        raise StopIteration
