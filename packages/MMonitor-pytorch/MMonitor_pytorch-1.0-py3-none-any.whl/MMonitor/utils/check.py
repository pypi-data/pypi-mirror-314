import torch
import torch.nn as nn

from ..quantity import QuantitySelector
from .schedules import ScheduleSelector


def _get_submodule(target, model):
    if target == "":
        return model

    atoms = target.split(".")
    mod = model

    for item in atoms:

        if not hasattr(mod, item):
            raise AttributeError(mod.__class__.__name__ + " has no attribute `" + item + "`")
        if isinstance(mod, nn.Sequential) or isinstance(mod, nn.ModuleList):
            mod = mod[int(item)]
        else:
            mod = getattr(mod, item)

        if not isinstance(mod, torch.nn.Module):
            raise AttributeError("`" + item + "` is not an nn.Module")

    return mod


def _is_module(module_name, module):
    if isinstance(module_name, str):
        if module.__class__.__name__ == module_name:
            return True
        else:
            return False
    elif isinstance(module_name, type):
        if isinstance(module, module_name):
            return True
        else:
            return False
    else:
        return False


def _check_name(module_name, model):
    try:
        mod = _get_submodule(module_name, model)
        return module_name
    except (AttributeError, TypeError):
        model_name = []
        for name, module in model.named_modules():
            if _is_module(module_name, module):
                model_name.append(name)
        return model_name
    

def _check_quantity(quantity_name):
    if isinstance(quantity_name, str):
        try:
            QuantitySelector.select(quantity_name)
            return quantity_name + '_linear(0, 0)'
        except NotImplementedError:
            return None
    track_schedule = '_'
    if len(quantity_name) == 1:
        track_schedule += 'linear(0, 0)'
    else:
        try:
            ScheduleSelector.select(quantity_name[1])
            track_schedule += quantity_name[1]
        except NotImplementedError:
            track_schedule = track_schedule + quantity_name[1] + '(error)'
    try:
        QuantitySelector.select(quantity_name[0])
        return quantity_name[0] + track_schedule
    except NotImplementedError:
        return None
    

def check_monitor_config(config, model):
    if isinstance(model, torch.nn.parallel.DistributedDataParallel):
        model = model.module
    msg = ""
    for model_name, quantitys in config.items():
        model_n = _check_name(model_name, model)
        msg += "(model)"
        if isinstance(model_n, str):
            msg = msg + model_n + ":"
        elif len(model_n) == 0:
            msg = model_name + "(error):"
        else:
            msg = '|'.join(model_n)
            msg += ':'
        quantity_name = []
        for quantity in quantitys:
            quantity_n = _check_quantity(quantity)
            if quantity_n is None:
                if isinstance(quantity, str):
                    quantity_name.append(quantity + '(error)')
                else:
                    quantity_name.append(quantity[0] + '(error)')
            else:
                quantity_name.append(quantity_n)
        msg = msg + '、'.join(quantity_name)
    return msg
    