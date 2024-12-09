
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os



class Figure:
    def __init__(self, data, name,ax=None, default_save_dir='./output/picture'):
        self.x_data = data[name]['x']
        self.y_data =  data[name]['y']
        self.x_label =  data[name]['x_label']
        self.y_label =  data[name]['y_label']
        self.legend =  data[name]['legend']
        self.title =  data[name]['title']
        self.figsize=(16, 10)
        self.dpi = 80
        self.ax = ax
        if self.ax is None:
            plt.figure(figsize=(16, 10), dpi=80)
            self.ax = plt.gca()
        self.default_save_dir = default_save_dir
        
    def plot(self, ax=None):
        ax = self._get_ax(ax)
        # self._pre_plot()
        self._plot(ax)
        self._finalize_plot(ax) 
    
    def show(self, ax=None):
        ax = self._get_ax(ax)
        ax.figure.canvas.draw()
    
    def save(self, file_name=None, save_dir=None, save_type='png'):
        dir = save_dir
        if dir is None:
            dir = self.default_save_dir
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_name = file_name
        if file_name is None:
            file_name = self.title + '.' + save_type
        file_path = os.path.join(dir, file_name)
        figure = plt.figure(figsize=(16, 10), dpi=80)
        ax = figure.add_subplot(1, 1, 1)
        self.plot(ax)
        figure.savefig(file_path)
        plt.close()

    def _get_ax(self, ax=None):
        if ax is None:
            return self.ax
        return ax
    
    def _plot(self, ax):
        raise NotImplementedError("Subclasses must implement the '_plot' method.")
    
    def _pre_plot(self):
        plt.figure(figsize=self.figsize, dpi=self.dpi)
        self.ax = plt.gca()
    
    def _finalize_plot(self, ax=None):
        self._set_xy(ax)
        self._set_title(ax)
        self._remove_borders(ax)
        ax.legend()
    
    def _set_title(self, ax=None):
        ax.set_title(self.title)
    
    def _set_xy(self, ax=None): 
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

    
    def _remove_borders(self, ax=None):

        # Remove borders
        ax.spines["top"].set_alpha(0.0)
        ax.spines["bottom"].set_alpha(0.3)
        ax.spines["right"].set_alpha(0.0)
        ax.spines["left"].set_alpha(0.3)
        
    def unsetlegend(self, ax=None):
        ax = self._get_ax(ax)
        ax.legend().set_visible(False)
        


    
    
    



    