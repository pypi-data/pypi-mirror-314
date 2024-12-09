# SPDX-FileCopyrightText: © 2024 Jimmy Fitzpatrick <jcfitzpatrick12@gmail.com>
# This file is part of SPECTRE
# SPDX-License-Identifier: GPL-3.0-or-later

from logging import getLogger
_LOGGER = getLogger(__name__)

import os
import time
from queue import Queue
from typing import Any
from abc import ABC, abstractmethod
from math import floor

from watchdog.events import FileSystemEventHandler

from spectre_core.chunks.factory import get_chunk_from_tag
from spectre_core.file_handlers.configs import CaptureConfig
from spectre_core.spectrograms.spectrogram import Spectrogram
from spectre_core.spectrograms.transform import join_spectrograms
from spectre_core.spectrograms.transform import (
    time_average, 
    frequency_average
)


class BaseEventHandler(ABC, FileSystemEventHandler):
    def __init__(self, 
                 tag: str, 
                 exception_queue: Queue, 
                 extension: str):
        self._tag = tag
        self._Chunk = get_chunk_from_tag(tag)

        self._capture_config = CaptureConfig(tag)

        self._extension = extension
        self._exception_queue = exception_queue  # Queue to propagate exceptions

        self._spectrogram: Spectrogram = None # spectrogram cache


    @abstractmethod
    def process(self, file_path: str) -> None:
        pass


    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(self._extension):
            _LOGGER.info(f"Noticed: {event.src_path}")
            try:
                self._wait_until_stable(event.src_path)
                self.process(event.src_path)
            except Exception as e:
                _LOGGER.error(f"An error has occured while processing {event.src_path}",
                              exc_info=True)
                self._flush_spectrogram() # flush the internally stored spectrogram
                # Capture the exception and propagate it through the queue
                self._exception_queue.put(e)


    def _wait_until_stable(self, file_path: str):
        _LOGGER.info(f"Waiting for file stability: {file_path}")
        size = -1
        while True:
            current_size = os.path.getsize(file_path)
            if current_size == size:
                _LOGGER.info(f"File is now stable: {file_path}")
                break  # File is stable when the size hasn't changed
            size = current_size
            time.sleep(0.25)


    def _average_in_time(self, spectrogram: Spectrogram) -> Spectrogram:
        requested_time_resolution = self._capture_config.get('time_resolution') # [s]
        if requested_time_resolution is None:
            raise KeyError(f"Time resolution has not been specified in the capture config!")
        average_over = floor(requested_time_resolution/spectrogram.time_resolution) if requested_time_resolution > spectrogram.time_resolution else 1
        return time_average(spectrogram, average_over)
    
    
    def _average_in_frequency(self, spectrogram: Spectrogram) -> Spectrogram:
        frequency_resolution = self._capture_config.get('frequency_resolution') # [Hz]
        if frequency_resolution is None:
            raise KeyError(f"Frequency resolution has not been specified in the capture config!")
        average_over = floor(frequency_resolution/spectrogram.frequency_resolution) if frequency_resolution > spectrogram.frequency_resolution else 1
        return frequency_average(spectrogram, average_over)
    

    def _join_spectrogram(self, spectrogram: Spectrogram) -> None:
        if self._spectrogram is None:
            self._spectrogram = spectrogram
        else:
            self._spectrogram = join_spectrograms([self._spectrogram, spectrogram])

        if self._spectrogram.time_range >= self._capture_config.get("joining_time"):
            self._flush_spectrogram()
    

    def _flush_spectrogram(self) -> None:
        if self._spectrogram:
            _LOGGER.info(f"Flushing spectrogram to file with chunk start time {self._spectrogram.chunk_start_time}")
            self._spectrogram.save()
            _LOGGER.info("Flush successful, resetting spectrogram cache")
            self._spectrogram = None # reset the cache