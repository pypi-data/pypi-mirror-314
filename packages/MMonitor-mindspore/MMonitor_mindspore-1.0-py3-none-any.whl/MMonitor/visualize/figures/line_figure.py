from .base_figure import *

class LineFigure(Figure):
    def __init__(self, x_data, y_data, legend=None, title=None, xlabel=None, ylabel=None, line_style='-', color=None):
        super().__init__(x_data, y_data, legend)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.line_style = line_style
        self.color = color

    def _plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        
        ax.plot(self.x_data, self.y_data, label=self.legend, linestyle=self.line_style, color=self.color)

        if self.title:
            ax.set_title(self.title)
        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)
        if self.legend:
            ax.legend()
        
        ax.grid(True)

    def show(self):
        plt.show()
