import os
import json
import pandas as pd
import jittor as jt
from collections import defaultdict
import numpy as np

class LoadTaskData:
    def __init__(self, root, task) -> None:
        self.task_file_path = os.path.join(root, task)
        self.project_filenames = [f for f in os.listdir(self.task_file_path) if os.path.isdir(os.path.join(self.task_file_path, f))]
        self.project_files_monitor = {}
        self.project_files_train = {}
        self.project_files_val = {}
        self.data = {}
        self._load_project_data()
        
    def _load_project_data(self):
        for project in self.project_filenames:
            dataloader = LoadProjectData(self.task_file_path, project)
            self.project_files_monitor[project] = dataloader.monitor_data
            self.project_files_train[project] = dataloader.train_data
            self.project_files_val[project] = dataloader.val_data
        self.data['monitor'] = self.project_files_monitor
        self.data['train'] = self.project_files_train
        self.data['val'] = self.project_files_val
            
    def load_data(self, quantity_name, data_type='monitor'):
        data = self.data[data_type].copy()
        if quantity_name is not None:
            if isinstance(quantity_name, str):
                data = {quantity_name: data[quantity_name]}
            elif isinstance(quantity_name, list):
                data = {key: data[key] for key in data if key in quantity_name} 
        return self._extract_quantity_data(data,quantity_name = quantity_name)
            
                
    def _get_project_name(self, project_name):
        if isinstance(project_name, str):
            project = self.project_files_monitor.get(project_name, None)
            if project is not None:
                return project_name 
            else:
                return None
        if isinstance(project_name, list):
            result = [self._get_project_name(i) for i in project_name]
            result = [i for i in result if i is not None]
            if len(result) == 0:
                return None
            return result
        
    def _extract_quantity_data(self, data,quantity_name):
        result = {}
        result['legend'] = list(data.keys())
        result_data = defaultdict(dict)
        for i in result['legend']:
            if i == quantity_name:
                df = data[i]
                result_data[i]['title'] = i
                result_data[i]['x_label'] = df.index.name
                result_data[i]['y_label'] = 'value'    
                result_data[i]['x'] = df.index.values
                # 对df[i].values进行改变
                result_len = len(df.index.values)
                values = jt.empty(result_len)
                for j in range(result_len):
                    result_num = df[i].values[j][0]
                    values[j] = result_num
                result_data[i]['y'] = values.numpy()
                result_data[i]['legend'] = i
        return result_data
    
    def get_project_name(self):
        return self.project_filenames
    
    def get_quantity_name(self, project_name=None, data_type='monitor'):
        data = self.data[data_type].copy()
        quantity_data = {}
        quantity_name = set()
        if project_name is not None:
            quantity_data[project_name] = data.get(project_name, None)
            if quantity_data[project_name] is None:
                quantity_data = data
        else:
            quantity_data = data
        for key in quantity_data:
            project_data = quantity_data[key]
            for name in project_data.columns:
                quantity_name.add(name)
        return quantity_name

class LoadProjectData:
    
    def __init__(self, local_path, task) -> None:
        self.local_path = local_path
        self.task = task
        self.monitor_filenames, self.train_filenames, self.val_filenames = self.load_filenames()
        self.monitor_data = self.load_filedata(self.monitor_filenames)
        self.train_data = self.load_filedata(self.train_filenames)
        self.val_data = self.load_filedata(self.val_filenames)
   
    def load_filenames(self):
        local_path = self.local_path
        monitor_filenames = []
        train_filenames = []
        val_filenames = []
        for _, dirnames, _ in os.walk(local_path):  
            for dirname in dirnames:
                current_dir = os.path.join(local_path,dirname)
                for _,_,filenames in os.walk(current_dir):
                    for filename in filenames:  
                        if filename.startswith('monitor'):
                            monitor_filenames.append(os.path.join(current_dir, filename))
                        if filename.startswith('train'):
                            train_filenames.append(os.path.join(current_dir, filename))
                        if filename.startswith('val'):
                            val_filenames.append(os.path.join(current_dir, filename))
        return monitor_filenames, train_filenames, val_filenames


    def load_filedata(self, filenames):
        files = []
        if filenames:
            for i in filenames:
                if self.task in i:
                    with open(i, 'r') as f:
                        files.append(json.load(f))
            df = pd.DataFrame(files) 
            df = df.sort_values(by='step')
            df = df.interpolate()
            df = df.dropna()
            df = df.set_index('step')
            return df
        else:
            return None