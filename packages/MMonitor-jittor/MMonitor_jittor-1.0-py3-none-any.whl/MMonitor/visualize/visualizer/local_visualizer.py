import os
import json
import numpy as np
import pandas as pd
from ..figures import *
from ..io_utils import *

class LocalVisualization:
    def __init__(self,dir='./output', project='task', save_dir='./output/picture', 
                figsize=(16, 10), dpi=80, ncols=3):
        self.dir = dir
        self.task = project
        self.save_dir = save_dir
        self.data_loader = LoadTaskData(root=self.dir, task=self.task)
        self.ncols = 3
        self.figsize = figsize
        self.dpi = dpi
        self.figure = None 

    def show(self, monitor,quantity_name=None,project_name=None, data_type='monitor'):
        figures,selected_quantity_name = self._plot(monitor,quantity_name,project_name,data_type)
        if figures is not None:
            for i, fig in enumerate(figures):
                file_name = f"{selected_quantity_name[i]}_result.png"
                fig.save(file_name=file_name)
            
        
    def _select_figure(self, data):
        return LineFigure

    
    def save(self, quantity_name, project_name=None, data_type='monitor',
             save_dir='./output/picture', file_name=None, save_type='png', save_subfigures=True):
        figures = self._plot(quantity_name, project_name,data_type)
        if figures is not None:
            dir = save_dir
            if dir is None:
                dir = self.save_dir
            if not os.path.exists(dir):
                os.makedirs(dir)
            file_name = file_name
            if file_name is None:
                file_name = quantity_name + '.' + save_type
            file_path = os.path.join(dir, file_name)
            self.figure.savefig(file_path)
            if save_subfigures:
                if len(figures) > 1:
                    for figure in figures:
                        figure.save()
        self._clear_figure()

        
    def get_project_name(self):
        return self.data_loader.get_project_name()
    
    def get_quantity_name(self, project_name, data_type='monitor'):
        return self.data_loader.get_quantity_name(project_name, data_type)
    
    def _cal_gridspe(self, num):
        nrows = num // self.ncols
        add = num % self.ncols != 0
        return nrows + add
    
    def _plot(self, monitor,quantity_name,project_name=None, data_type='monitor'):
        figures = []
        selected_quantity_name = []
        pro = list(monitor.get_output().keys())[0]
        if quantity_name is None:
            for name in self.get_quantity_name(project_name, data_type):
                selected_quantity_name.append(name)
        else:
            quantity_name = pro+'_'+quantity_name
            selected_quantity_name.append(quantity_name)
        nrows = self._cal_gridspe(len(selected_quantity_name))
        print(f"selected_quantity_name:{selected_quantity_name}")
        if self.figure is None:
            fcal, frow = self.figsize
            self.figure = plt.figure(figsize=(fcal, frow*nrows), dpi=self.dpi)
        if len(selected_quantity_name) > 1:
            for i, name in enumerate(selected_quantity_name):
                data = self.data_loader.load_data(name, data_type)
                figure = self._select_figure(data)(data, name)
                figure.plot()
                figures.append(figure)
        elif len(selected_quantity_name) == 1:
            name = selected_quantity_name[0]
            data = self.data_loader.load_data(selected_quantity_name[0], data_type)
            # ax = self.figure.add_subplot()
            figure = self._select_figure(data)(data, name)
            figure.plot()
            figures.append(figure)
        else:
            return None
        return figures,selected_quantity_name
    
    def _clear_figure(self):
        self.figure = None