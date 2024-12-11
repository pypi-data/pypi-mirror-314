# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.
from __future__ import annotations

import logging
from uuid import UUID

from lima2.client.devencoded import dense_frame, sparse_frame, structured_array
from lima2.client.processing import Processing as Base
from lima2.client.processing import Topology

# Create a logger
_logger = logging.getLogger(__name__)


class Processing(Base):
    tango_class = "LimaProcessingXpcs"

    def __init__(
        self,
        uuid: UUID,
        proc_urls: list[str],
        topology: Topology,
        timeout: int = Base.DEFAULT_TANGO_TIMEOUT,
    ):
        super().__init__(
            uuid=uuid, proc_urls=proc_urls, topology=topology, timeout=timeout
        )

    @property
    def channels(self) -> dict:
        """Returns the channels frame info"""
        # Lets assume same processing on each receivers
        return {
            "input_frame": self.input_frame_info[0],
            "frame": self.processed_frame_info[0],
            "sparse_frame": self.processed_frame_info[0],
        }

    def pop_roi_statistics(self):
        """
        Pop a list of Roi Statistics for each processing devices


        Returns:
            A list of roi statistics dict or [] if no value available
        """
        dtype = [
            ("min", "f4"),
            ("max", "f4"),
            ("avg", "f4"),
            ("std", "f4"),
            ("sum", "f8"),
        ]
        counters = [
            structured_array.decode(dev.popRoiStatistics(), dtype)
            for dev in self.__devs
        ]

        # TODO Round-Robin mode - compute frame_idx
        _logger.debug(f"pop_roi_statistics() -> {counters}")

        # If all devices have empty ROI counter list, then empty and returns an empty iterable
        return [] if not all([c.size > 0 for c in counters]) else counters

    @property
    def nb_roi_statistics(self):
        return [dev.nb_roi_statistics for dev in self.__devs]

    def pop_roi_profiles(self):
        """
        Pop a list of Roi Profiles for each processing devices


        Returns:
            A list of roi profiles dict or [] if no counter available
        """
        dtype = [
            ("min", "f4"),
            ("max", "f4"),
            ("avg", "f4"),
            ("std", "f4"),
            ("sum", "f8"),
        ]
        counters = [
            structured_array.decode(dev.popRoiProfiles(), dtype) for dev in self.__devs
        ]

        # TODO Round-Robin mode - compute frame_idx
        _logger.debug(f"pop_roi_profiles() -> {counters}")

        # If all devices have empty ROI counter list, then empty and returns an empty iterable
        return [] if not all([c.size > 0 for c in counters]) else counters

    @property
    def nb_roi_profiles(self):
        return [dev.nb_roi_profiles for dev in self.__devs]

    def pop_fill_factors(self):
        """
        Pop a list of Fill Factors for each processing devices


        Returns:
            A list of fill factors dict or [] if no value available
        """
        counters = [dev.popFillFactors() for dev in self.__devs]

        # TODO Round-Robin mode - compute frame_idx
        _logger.debug(f"pop_fill_factors() -> {counters}")

        # If all devices have empty ROI counter list, then empty and returns an empty iterable
        return [] if not all([c.size > 0 for c in counters]) else counters

    @property
    def nb_fill_factors(self):
        return [dev.nb_fill_factors for dev in self.__devs]

    def get_frame(self, frame_idx, source="frame"):
        # TODO let Flint know that this source does not have a buffer (cant be displayed)
        if source == "raw_frame":
            raise NotImplementedError("Frame not available for 'raw_frame'")

        frame_mapping = {
            "frame": {"getter": "getFrame", "decoder": dense_frame},
            "input_frame": {"getter": "getInputFrame", "decoder": dense_frame},
            "sparse_frame": {"getter": "getSparseFrame", "decoder": sparse_frame},
        }

        if source not in frame_mapping:
            raise ValueError(f"Invalid source name '{source}'")

        getter, decoder = frame_mapping[source].values()

        # TODO Round-Robin mode - select receiver that has frame_idx
        frames = [
            decoder.decode(getattr(dev, getter)(frame_idx)) for dev in self.__devs
        ]
        frames = [f for f in frames if f is not None]

        return frames[0] if len(frames) > 0 else None
