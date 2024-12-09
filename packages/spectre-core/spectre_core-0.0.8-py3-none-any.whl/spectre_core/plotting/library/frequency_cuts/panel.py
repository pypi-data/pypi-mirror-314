# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
from datetime import datetime

from spectre_core.spectrograms.spectrogram import FrequencyCut
from spectre_core.spectrograms.spectrogram import Spectrogram
from spectre_core.plotting.base import BaseSpectrumPanel, CutsPanel
from spectre_core.plotting.panel_register import register_panel
from spectre_core.plotting.format import DEFAULT_FORMATS

FREQUENCY_CUTS_PANEL_NAME = "frequency_cuts"

@register_panel(FREQUENCY_CUTS_PANEL_NAME)
class Panel(BaseSpectrumPanel, CutsPanel):
    def __init__(self, 
                 name: str,
                 spectrogram: Spectrogram, 
                 time_type: str = "seconds",
                 *times: list[float | str],
                 dBb: bool = False,
                 peak_normalise: bool = False,
                 cmap: str = DEFAULT_FORMATS.cuts_cmap,
                 **kwargs):
        super().__init__(name, 
                         spectrogram, 
                         time_type, 
                         **kwargs)
        self._times = times
        self._cmap = cmap
        self._dBb = dBb
        self._peak_normalise = peak_normalise
        # map each time cut to the corresponding FrequencyCut dataclass
        self._frequency_cuts: Optional[dict[float | datetime, FrequencyCut]] = {}


    @property
    def frequency_cuts(self) -> dict[float | str, FrequencyCut]:
        if not self._frequency_cuts:
            for time in self._times:
                frequency_cut = self._spectrogram.get_frequency_cut(time,
                                                                    dBb = self._dBb,
                                                                    peak_normalise = self._peak_normalise)
                self._frequency_cuts[frequency_cut.time] = frequency_cut
        return self._frequency_cuts


    @property
    def times(self) -> list[float | datetime]:
        return list(self.frequency_cuts.keys())
    

    def draw(self):
        for time, color in self.bind_to_colors():
            frequency_cut = self.frequency_cuts[time]
            self.ax.step(self.frequencies*1e-6, # convert to MHz
                         frequency_cut.cut, 
                         where='mid', 
                         color = color)
    

    def annotate_y_axis(self) -> None:
        if self._dBb:
            self.ax.set_ylabel('dBb')
        elif self._peak_normalise:
            return # no y-axis label
        else:
            self.ax.set_ylabel(f'{self._spectrogram.spectrum_type.capitalize()}')

    
    def bind_to_colors(self):
        return super().bind_to_colors(self.times, cmap = self._cmap)