#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import signal
from argparse import ArgumentParser
from typing import Any

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import spectre

from spectre_core.cfg import CHUNKS_DIR_PATH
from spectre_core.file_handlers.configs import CaptureConfig

class tagged_staircase(gr.top_block):

    def __init__(self, 
                 capture_config: CaptureConfig):
        gr.top_block.__init__(self, "tagged-staircase", catch_exceptions=True)

        ##################################################
        # Unpack capture config
        ##################################################
        tag = capture_config['tag']
        step_increment = capture_config['step_increment']
        samp_rate = capture_config['samp_rate']
        min_samples_per_step = capture_config['min_samples_per_step']
        max_samples_per_step = capture_config['max_samples_per_step']
        freq_step = capture_config['freq_step']
        chunk_size = capture_config['chunk_size']
        is_sweeping = True

        ##################################################
        # Blocks
        ##################################################
        self.spectre_tagged_staircase_0 = spectre.tagged_staircase(min_samples_per_step, 
                                                                   max_samples_per_step, 
                                                                   freq_step,
                                                                   step_increment, 
                                                                   samp_rate)
        self.spectre_batched_file_sink_0 = spectre.batched_file_sink(CHUNKS_DIR_PATH,
                                                                     tag, 
                                                                     chunk_size, 
                                                                     samp_rate, 
                                                                     is_sweeping,
                                                                     'rx_freq',
                                                                     0
                                                                     )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate, True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.spectre_batched_file_sink_0, 0))
        self.connect((self.spectre_tagged_staircase_0, 0), (self.blocks_throttle_0, 0))




def main(capture_config: CaptureConfig, 
         top_block_cls=tagged_staircase, 
         options=None):
    tb = top_block_cls(capture_config)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()