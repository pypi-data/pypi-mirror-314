# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import numpy as np
from torch.nn import Dropout, Dropout2d


class DropoutScheduler:
    def __init__(self, models, T=5e4):
        """
        T: number of gradient updates to converge
        """

        self.teta_list = list()
        self.init_teta_list(models)
        self.T = T
        self.step_num = 0

    def step(self, num):
        self.step_num += num

    def resume(self, step_num):
        self.step_num = step_num

    def init_teta_list(self, models):
        for model_name in models:
            self.init_teta_list_module(models[model_name])

    def init_teta_list_module(self, module):
        for child in module.children():
            if isinstance(child, Dropout) or isinstance(child, Dropout2d):
                self.teta_list.append([child, child.p])
            else:
                self.init_teta_list_module(child)

    def update_dropout_rate(self):
        for module, p in self.teta_list:
            module.p = exponential_dropout_scheduler(p, self.step_num, self.T)


def exponential_dropout_scheduler(dropout_rate, step, max_step):
    return dropout_rate * (1 - np.exp(-10 * step / max_step))


def exponential_scheduler(init_value, end_value, step, max_step):
    step = min(step, max_step - 1)
    return init_value - (init_value - end_value) * (1 - np.exp(-10 * step / max_step))
