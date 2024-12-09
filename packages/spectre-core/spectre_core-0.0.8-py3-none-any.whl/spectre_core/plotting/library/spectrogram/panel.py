# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from warnings import warn

from spectre_core.plotting.base import BaseTimeSeriesPanel
from spectre_core.plotting.panel_register import register_panel
from spectre_core.plotting.base import CutsPanel
from spectre_core.plotting.library.time_cuts.panel import Panel as TimeCutsPanel
from spectre_core.plotting.library.frequency_cuts.panel import Panel as FrequencyCutsPanel
from spectre_core.plotting.format import DEFAULT_FORMATS

SPECTROGRAM_PANEL_NAME = "spectrogram"

@register_panel(SPECTROGRAM_PANEL_NAME)
class Panel(BaseTimeSeriesPanel):
    def __init__(self, 
                 *args, 
                 log_norm: bool = False,
                 dBb: bool = False,
                 vmin: float | None = -1,
                 vmax: float | None = 2,
                 cmap: str = DEFAULT_FORMATS.spectrogram_cmap,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._log_norm = log_norm
        self._dBb = dBb
        self._vmin = vmin
        self._vmax = vmax
        self._cmap = cmap


    def draw(self):
        dynamic_spectra = self._spectrogram.dynamic_spectra_as_dBb if self._dBb else self._spectrogram.dynamic_spectra

        norm = LogNorm(vmin=np.nanmin(dynamic_spectra[dynamic_spectra > 0]), 
                       vmax=np.nanmax(dynamic_spectra)) if self._log_norm else None
        

        if self._log_norm and (self._vmin or self._vmax):
            warn("vmin/vmax will be ignored while using log_norm.")
            self._vmin = None 
            self._vmax = None
        
        # Plot the spectrogram with kwargs
        pcm = self.ax.pcolormesh(self.times, 
                            self._spectrogram.frequencies * 1e-6, 
                            dynamic_spectra,
                            vmin=self._vmin, 
                            vmax=self._vmax,
                            norm=norm, 
                            cmap=self._cmap)
        
        # Add colorbar if dBb is used
        if self._dBb:
            cbar = self.fig.colorbar(pcm, 
                                      ax=self.ax, 
                                      ticks=np.linspace(self._vmin, self._vmax, 6, dtype=int))
            cbar.set_label('dBb')


    def annotate_y_axis(self) -> None:
        self.ax.set_ylabel('Frequency [MHz]')
        return
    
    
    def overlay_cuts(self, cuts_panel: CutsPanel) -> None:
        if isinstance(cuts_panel, TimeCutsPanel):
            self._overlay_time_cuts(cuts_panel)
        elif isinstance(cuts_panel, FrequencyCutsPanel):
            self._overlay_frequency_cuts(cuts_panel)


    def _overlay_time_cuts(self, time_cuts_panel: TimeCutsPanel) -> None:
        for frequency, color in time_cuts_panel.bind_to_colors():
            self.ax.axhline(frequency*1e-6, # convert to MHz
                            color = color,
                            linewidth=DEFAULT_FORMATS.line_width
                            )
            
            
    def _overlay_frequency_cuts(self, frequency_cuts_panel: FrequencyCutsPanel) -> None:
        for time, color in frequency_cuts_panel.bind_to_colors():
            self.ax.axvline(time,
                            color = color,
                            linewidth=DEFAULT_FORMATS.line_width
                            )
