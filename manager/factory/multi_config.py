from manager.factory.input_config import *
import itertools


class multi_config:
    alphas_ = [1]
    momenta_ = [0]
    factory_ = input_config()

    def build(self):
        items = list(itertools.product(self.alphas_, self.momenta_))
        params = ["alpha", "momentum"]
        self.elements_ = []
        for item in items:
            self.elements_.append(dict(zip(params, item)))

    def alphas(self, a):
        self.alphas_ = a
        return self

    def momenta(self, p):
        self.momenta_ = p
        return self

    def get_config(self, element):
        kwargs = {
            "/Configuration/alpha_": element["alpha"],
            "/Configuration/global_p_mod_": element["momentum"]
        }
        return self.factory_.generate(**kwargs)

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
