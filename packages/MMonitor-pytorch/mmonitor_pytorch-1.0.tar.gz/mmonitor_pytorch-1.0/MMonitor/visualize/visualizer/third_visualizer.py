
from collections import defaultdict

import os
import json
import numpy as np
import torch


class Visualization:
    def __init__(self, monitor=None, dir='./output', project='task', name='name',is_tf = None):
        self.clean_step = 500
        self.dir = dir
        self.monitor = monitor
        self.project = list(project)[0].__name__
        self.name = list(name)[0]
        self.save_dir = os.path.join(self.dir, self.project)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    # save to local
    def show(self, step, ext=None):
        logs = defaultdict(dict)
        save_logs = defaultdict(dict)
        module_names = self._get_module_name()
        for module_name in module_names:
            quantitis = self.monitor.parse_quantity[module_name]
            quantity_names = self._get_quantity_name(module_name)
            for quantity, quantity_name in zip(quantitis, quantity_names):
                if not quantity.should_show(step):
                    continue
                key = module_name + '_' + quantity_name
                save_dir = os.path.join(self.save_dir,key)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                val = self._get_result(module_name, quantity_name, step)
                save_logs[key] = val
                if val.size == 1:
                    val = val.item()
                else:
                    val = self._get_result(module_name, quantity_name)
                logs[key] = val
        if ext is not None:
            logs.update(ext)
        self.save_to_local(step, save_logs)
        return logs
    
    def save_to_local(self, step=0, data_log=None, log_type='monitor'):
        if data_log is not None and len(data_log) != 0:
            self._save(step, data_log, log_type)
    
    def _save(self, step, data_log, log_type):
        # print(data_log)
        data_log['step'] = step
        data_log= self._apply_save_format(data_log) 
        for task in data_log.keys():
            result_log = defaultdict(dict)
            if task != 'step':
                file_name = os.path.join(self.save_dir,task,log_type + '_' + str(step) + '.json')
                result = data_log[task]
                result_log[task] = result
                result_log['step'] = step
                with open(file_name, 'w') as f:
                    json.dump(result_log, f)
    
    def log_ext(self, step=None, ext=None, log_type='train'):
        self.vis.log(ext)
        self.save_to_local(step, ext, log_type)

    def _get_module_name(self):
        module_names = self.monitor.get_output().keys()
        return module_names

    def _get_quantity_name(self, module_name):
        quantity_name = self.monitor.get_output()[module_name].keys()
        return quantity_name

    def _get_result(self, module_name, quantity_name, step=None):
        if step != None:
            value = self.monitor.get_output()[module_name][quantity_name][step]
        else:
            value = self.monitor.get_output()[module_name][quantity_name]
        return value
    
    
    def _apply_save_format(self, value):
        """Apply formatting rules for saved data.

        ``torch.Tensor``s are detached, loaded to CPU and converted to ``numpy`` arrays.
        Items of ``dict``, ``list``, and ``tuple`` are converted recursively.
        ``float``, ``int``, and ``numpy.ndarray`` values are unaffected.

        Args:
            value (Any): Value to be saved.

        Returns:
            Any: Converted value.

        Raises:
            NotImplementedError: If there is no formatting rule for the data type.
        """
        if isinstance(value, torch.Tensor):
            value = self._apply_save_format(value.detach().cpu().numpy())

        elif isinstance(value, dict):
            for key, val in value.items():
                value[key] = self._apply_save_format(val)

        elif isinstance(value, list):
            for idx, val in enumerate(value):
                value[idx] = self._apply_save_format(val)
        elif isinstance(value, (np.ndarray)):
            value = value.tolist()

        elif isinstance(value, tuple):
            value = tuple(self._apply_save_format(val) for val in value)

        elif isinstance(value, (np.float32)):
            value = value.float()
        elif isinstance(value, (float, int)):
            pass
        else:
            raise NotImplementedError(f"No formatting rule for type {type(value)}")

        return value
