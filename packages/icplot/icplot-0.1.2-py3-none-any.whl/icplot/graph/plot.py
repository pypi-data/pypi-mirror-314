"""
This module has content for generating plots
"""

import random

from pydantic import BaseModel

from icplot.color import ColorMap, Color

from .axis import PlotAxis
from .series import PlotSeries


class Plot(BaseModel, frozen=True):
    """
    A generic plot with optional axis ticks
    """

    title: str = ""
    legend_label: str = ""
    name: str = ""
    x_axis: PlotAxis = PlotAxis()
    y_axes: list[PlotAxis] = [PlotAxis()]
    plot_type: str = ""
    series: list[PlotSeries] = []
    legend: str = "none"


class GridPlot(Plot, frozen=True):
    """
    Make a grid of plots
    """

    stride: int = 4
    size: tuple = (25, 20)
    data: list = []

    def get_series_indices(self, num_samples: int = 0):
        rows = num_samples // self.stride
        cols = num_samples // rows
        len_data = len(self.data)

        if num_samples == 0:
            indices = list(range(0, len_data))
        else:
            indices = [random.randint(0, len_data - 1) for _ in range(num_samples)]
        return rows, cols, indices

    def get_subplots(self, num_samples: int = 0):
        rows, cols, indices = self.get_series_indices(num_samples)

        subplots = []
        count = 1
        for index in indices:
            if num_samples > 0 and count == num_samples + 1:
                break
            if isinstance(self.data[index], list):
                for series in self.data[index]:
                    subplots.append(series)
                    count += 1
            else:
                subplots.append(self.data[index])
                count += 1
        return rows, cols, subplots


def get_series_colors(cmap: ColorMap, plot: Plot) -> list[Color | None]:

    count = 0
    num_colorable = len([s for s in plot.series if not s.highlight])
    colors = []
    for s in plot.series:
        if not s.highlight:
            color = cmap.get_color(count, num_colorable)
            count = count + 1
        else:
            color = None
        colors.append(color)
    return colors
