from collections import defaultdict
import os
import json
import numpy as np
import jittor as jt

class Visualization:
    def __init__(self, monitor=None, dir='./output', project='task', name='name'):
        self.clean_step = 500
        self.dir = dir
        self.monitor = monitor
        self.project = list(project)[0].__name__
        self.name = list(name)[0]
        self.save_dir = os.path.join(self.dir, self.project)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    # Save to local
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
                key = f"{module_name}_{quantity_name}"
                save_dir = os.path.join(self.save_dir, key)
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
        data_log['step'] = step
        data_log = self._apply_save_format(data_log) 
        for task in data_log.keys():
            result_log = defaultdict(dict)
            if task != 'step':
                file_name = os.path.join(self.save_dir, task, f"{log_type}_{step}.json")
                result = data_log[task]
                result_log[task] = result
                result_log['step'] = step
                with open(file_name, 'w') as f:
                    json.dump(result_log, f)

    def log_ext(self, step=None, ext=None, log_type='train'):
        self.save_to_local(step, ext, log_type)

    def _get_module_name(self):
        return self.monitor.get_output().keys()

    def _get_quantity_name(self, module_name):
        return self.monitor.get_output()[module_name].keys()

    def _get_result(self, module_name, quantity_name, step=None):
        if step is not None:
            value = self.monitor.get_output()[module_name][quantity_name][step]
        else:
            value = self.monitor.get_output()[module_name][quantity_name]
        return value
    
    def _apply_save_format(self, value):
        """Apply formatting rules for saved data.

        Jittor tensors are converted to NumPy arrays for saving.

        Args:
            value (Any): Value to be saved.

        Returns:
            Any: Converted value.

        Raises:
            NotImplementedError: If there is no formatting rule for the data type.
        """
        # 检查是否为 Jittor Var
        if isinstance(value, jt.Var):
            # 转换为 numpy 数组
            value = value.numpy()

        elif isinstance(value, dict):
            # 对字典中的每个值递归应用格式转换
            for key, val in value.items():
                value[key] = self._apply_save_format(val)

        elif isinstance(value, list):
            # 对列表中的每个值递归应用格式转换
            for idx, val in enumerate(value):
                value[idx] = self._apply_save_format(val)

        elif isinstance(value, np.ndarray):
            # 将 numpy 数组转换为 Python 列表
            value = value.tolist()

        elif isinstance(value, tuple):
            # 对元组中的每个值递归应用格式转换
            value = tuple(self._apply_save_format(val) for val in value)

        elif isinstance(value, np.float32):
            # 如果是 np.float32 类型，转换为 Jittor 的 float 类型
            value = jt.float32(value)

        elif isinstance(value, (float, int)):
            # 如果是原生 Python 的 float 或 int 类型，保持原样
            pass

        else:
            # 其他未处理类型，抛出异常
            raise NotImplementedError(f"No formatting rule for type {type(value)}")

        return value