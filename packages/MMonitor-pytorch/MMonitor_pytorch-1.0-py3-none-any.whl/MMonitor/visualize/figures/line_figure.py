from .base_figure import *

class LineFigure(Figure):
    def _plot(self, ax=None):
        ax.plot(self.x_data, self.y_data, label=self.legend)

            
   