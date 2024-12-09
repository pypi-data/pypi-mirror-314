# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

from logging import getLogger
_LOGGER = getLogger(__name__)

import os

from spectre_core.watchdog.base import BaseEventHandler
from spectre_core.watchdog.event_handler_register import register_event_handler

@register_event_handler("fixed")
class EventHandler(BaseEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def process(self, file_path: str):
        _LOGGER.info(f"Processing: {file_path}")
        file_name = os.path.basename(file_path)
        chunk_start_time, _ = os.path.splitext(file_name)[0].split('_')
        chunk = self._Chunk(chunk_start_time, self._tag)

        _LOGGER.info("Creating spectrogram")
        spectrogram = chunk.build_spectrogram()

        _LOGGER.info("Averaging spectrogram")
        spectrogram = self._average_in_time(spectrogram)
        spectrogram = self._average_in_frequency(spectrogram)

        _LOGGER.info("Joining spectrogram")
        self._join_spectrogram(spectrogram)

        bin_chunk = chunk.get_file('bin')
        _LOGGER.info(f"Deleting {bin_chunk.file_path}")
        bin_chunk.delete()

        hdr_chunk = chunk.get_file('hdr')
        _LOGGER.info(f"Deleting {hdr_chunk.file_path}")
        hdr_chunk.delete()
