# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

from spectre_core.plotting.base import BaseTimeSeriesPanel
from spectre_core.plotting.panel_register import register_panel
from spectre_core.plotting.format import DEFAULT_FORMATS

INTEGRAL_OVER_FREQUENCY_PANEL_NAME = "integral_over_frequency"

@register_panel(INTEGRAL_OVER_FREQUENCY_PANEL_NAME)
class Panel(BaseTimeSeriesPanel):
    def __init__(self, 
                 *args, 
                 peak_normalise: bool = False,
                 background_subtract: bool = False,
                 color: str = DEFAULT_FORMATS.integral_over_frequency_color,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._peak_normalise = peak_normalise
        self._background_subtract = background_subtract
        self._color = color


    def draw(self):
        I = self._spectrogram.integrate_over_frequency(correct_background = self._background_subtract,
                                                       peak_normalise = self._peak_normalise)
        self.ax.step(self.times, I, where="mid", color = self._color)
 

    def annotate_y_axis(self):
        return # no y-axis label

    
