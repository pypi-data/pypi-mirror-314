# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy as np
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from spectre_core.spectrograms.spectrogram import Spectrogram
from spectre_core.plotting.base import BasePanel, CutsPanel
from spectre_core.plotting.format import DEFAULT_FORMATS
from spectre_core.plotting.factory import get_panel
from spectre_core.plotting.library.spectrogram.panel import Panel as SpectrogramPanel

class PanelStack:
    def __init__(self, time_type: str, figsize: Tuple[int, int] = (10, 10)):
        self._time_type = time_type
        self._figsize = figsize
        self._panels: List[BasePanel] = []
        self._superimposed_panels: List[BasePanel] = []
        self._fig: Optional[Figure] = None
        self._axs: Optional[np.ndarray[Axes]] = None


    @property
    def time_type(self) -> str:
        return self._time_type


    @property
    def panels(self) -> List[BasePanel]:
        return sorted(self._panels, key=lambda panel: panel.x_axis_type)


    @property
    def fig(self) -> Optional[Figure]:
        return self._fig


    @property
    def axs(self) -> Optional[np.ndarray[Axes]]:
        return np.atleast_1d(self._axs)


    @property
    def num_panels(self) -> int:
        return len(self._panels)


    def add_panel(self, 
                  panel_name: str, 
                  spectrogram: Spectrogram,
                  *args, 
                  identifier: Optional[str] = None,
                  **kwargs) -> None:
        panel = get_panel(panel_name, 
                          spectrogram, 
                          self._time_type, 
                          *args, 
                          **kwargs)
        if identifier: 
            panel.identifier = identifier
        self._panels.append(panel)


    def superimpose_panel(self, 
                          panel_name: str, 
                          spectrogram: Spectrogram, 
                          *args, 
                          identifier: Optional[str] = None,
                          **kwargs) -> None:
        panel = get_panel(panel_name, 
                          spectrogram, 
                          self._time_type, 
                          *args, 
                          **kwargs)
        if identifier:
            panel.identifier = identifier
        self._superimposed_panels.append(panel)


    def _init_plot_style(self) -> None:
        plt.style.use(DEFAULT_FORMATS.style)
        plt.rc('font', size=DEFAULT_FORMATS.small_size)
        plt.rc('axes', titlesize=DEFAULT_FORMATS.medium_size, 
                       labelsize=DEFAULT_FORMATS.medium_size)
        plt.rc('xtick', labelsize=DEFAULT_FORMATS.small_size)
        plt.rc('ytick', labelsize=DEFAULT_FORMATS.small_size)
        plt.rc('legend', fontsize=DEFAULT_FORMATS.small_size)
        plt.rc('figure', titlesize=DEFAULT_FORMATS.large_size)


    def _create_figure_and_axes(self) -> None:
        self._fig, self._axs = plt.subplots(self.num_panels, 1, figsize=self._figsize, layout="constrained")


    def _assign_axes(self) -> None:
        shared_axes = {}
        for i, panel in enumerate(self.panels):
            panel.ax = self.axs[i]
            panel.fig = self._fig
            if panel.x_axis_type in shared_axes:
                panel.ax.sharex(shared_axes[panel.x_axis_type])
            else:
                shared_axes[panel.x_axis_type] = panel.ax


    def _overlay_cuts(self, cuts_panel: CutsPanel) -> None:
        """Given a cuts panel, finds any corresponding spectrogram panels and adds the appropriate overlay"""
        for panel in self.panels:
            is_corresponding_panel = isinstance(panel, SpectrogramPanel) and (panel.tag == cuts_panel.tag)
            if is_corresponding_panel:
                panel.overlay_cuts(cuts_panel)


    def _overlay_superimposed_panels(self) -> None:
        for super_panel in self._superimposed_panels:
            for panel in self._panels:
                if panel.name == super_panel.name and (panel.identifier == super_panel.identifier): # find the matching panels via panel names
                    super_panel.ax, super_panel.fig = panel.ax, self._fig # and superimpose via axes sharing
                    super_panel.draw()
                    if isinstance(super_panel, CutsPanel):
                        self._overlay_cuts(super_panel)


    def show(self) -> None:
        self._init_plot_style()
        self._create_figure_and_axes()
        self._assign_axes()
        last_panel_per_axis = {panel.x_axis_type: panel for panel in self.panels}
        for panel in self.panels:
            panel.draw()
            panel.annotate_y_axis()
            if panel == last_panel_per_axis[panel.x_axis_type]:
                panel.annotate_x_axis()
            else:
                panel.hide_x_axis_labels()
            if isinstance(panel, CutsPanel):
                        self._overlay_cuts(panel)


        self._overlay_superimposed_panels()
        plt.show()
