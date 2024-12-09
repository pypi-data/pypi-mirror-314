from .singlestep import *
from .multistep import *


class QuantitySelector:

    @staticmethod
    def select(quantity_name):
        if quantity_name not in globals():
            raise NotImplementedError(
                "hook not found: {}".format(quantity_name))
        quantity = globals()[quantity_name]
        return quantity
