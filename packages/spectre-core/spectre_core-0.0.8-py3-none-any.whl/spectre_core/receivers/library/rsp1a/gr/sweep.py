#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

import sys
import signal
from argparse import ArgumentParser
from typing import Any

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import sdrplay3
from gnuradio import spectre

from spectre_core.cfg import CHUNKS_DIR_PATH
from spectre_core.file_handlers.configs import CaptureConfig


class sweep(gr.top_block):
    def __init__(self, 
                 capture_config: CaptureConfig):
        gr.top_block.__init__(self, "sweep", catch_exceptions=True)

        ##################################################
        # Unpack capture config
        ##################################################
        samp_rate = capture_config['samp_rate']
        bandwidth = capture_config['bandwidth']
        min_freq = capture_config['min_freq']
        max_freq = capture_config['max_freq']
        freq_step = capture_config['freq_step']
        samples_per_step = capture_config['samples_per_step']
        IF_gain = capture_config['IF_gain']
        RF_gain = capture_config['RF_gain']
        chunk_size = capture_config['chunk_size']
        start_freq = min_freq + samp_rate/2
        tag = capture_config['tag']

        ##################################################
        # Blocks
        ##################################################
        self.spectre_sweep_driver_0 = spectre.sweep_driver(min_freq, 
                                                           max_freq, 
                                                           freq_step, 
                                                           samp_rate, 
                                                           samples_per_step,
                                                           'freq')
        self.spectre_batched_file_sink_0 = spectre.batched_file_sink(CHUNKS_DIR_PATH, 
                                                                     tag, 
                                                                     chunk_size, 
                                                                     samp_rate, 
                                                                     True, 
                                                                     'freq', 
                                                                     start_freq)
        self.sdrplay3_rsp1a_0 = sdrplay3.rsp1a(
            '',
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=1
            ),
        )
        self.sdrplay3_rsp1a_0.set_sample_rate(samp_rate, True)
        self.sdrplay3_rsp1a_0.set_center_freq(start_freq, True)
        self.sdrplay3_rsp1a_0.set_bandwidth(bandwidth)
        self.sdrplay3_rsp1a_0.set_gain_mode(False)
        self.sdrplay3_rsp1a_0.set_gain(IF_gain, 'IF', True)
        self.sdrplay3_rsp1a_0.set_gain(RF_gain, 'RF', True)
        self.sdrplay3_rsp1a_0.set_freq_corr(0)
        self.sdrplay3_rsp1a_0.set_dc_offset_mode(False)
        self.sdrplay3_rsp1a_0.set_iq_balance_mode(False)
        self.sdrplay3_rsp1a_0.set_agc_setpoint(-30)
        self.sdrplay3_rsp1a_0.set_rf_notch_filter(False)
        self.sdrplay3_rsp1a_0.set_dab_notch_filter(False)
        self.sdrplay3_rsp1a_0.set_biasT(False)
        self.sdrplay3_rsp1a_0.set_stream_tags(True)
        self.sdrplay3_rsp1a_0.set_debug_mode(False)
        self.sdrplay3_rsp1a_0.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rsp1a_0.set_show_gain_changes(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.spectre_sweep_driver_0, 'freq'), (self.sdrplay3_rsp1a_0, 'freq'))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.spectre_batched_file_sink_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.spectre_sweep_driver_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.sdrplay3_rsp1a_0.set_sample_rate(self.samp_rate, True)




def main(capture_config: CaptureConfig, 
         top_block_cls=sweep, 
         options=None):
    
    tb = top_block_cls(capture_config)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start(512)

    tb.wait()


if __name__ == '__main__':
    main()
