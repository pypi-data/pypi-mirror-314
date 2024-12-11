# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.
from __future__ import annotations

import logging
from uuid import UUID

from lima2.client.devencoded import (
    dense_frame,
    sparse_frame,
    structured_array,
)
from lima2.client.processing import Processing as Base
from lima2.client.processing import Topology

# Create a logger
_logger = logging.getLogger(__name__)


class Processing(Base):
    tango_class = "LimaProcessingSmx"

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
    def radius1d(self):
        """Returns the radius1d"""
        return [dense_frame.decode(dev.radius1d).data for dev in self.__devs]

    @property
    def radius2d_mask(self):
        """Returns the radius2d_mask as np.array"""
        return [dense_frame.decode(dev.radius2d_mask).data for dev in self.__devs]

    def popRoiCounters(self, nb_frames):
        """Pop a list of RoiCounters for each devices or None if no counter is extracted"""
        dtype = [
            ("frame_idx", "i8"),
            ("min", "f4"),
            ("max", "f4"),
            ("avg", "f4"),
            ("std", "f4"),
            ("sum", "f8"),
        ]
        counters = [
            structured_array.decode(dev.popRoiCounters(nb_frames), dtype)
            for dev in self.__devs
        ]

        # TODO Round-Robin mode - compute frame_idx

        # If all devices have empty ROI counter list, then empty and returns an empty iterable
        return [] if not all([c.size > 0 for c in counters]) else counters

    def popPeakCounters(self, nb_frames):
        """Pop a list of peaks counter for each devices or None if no counter is extracted"""
        counters = [dev.popPeakCounters(nb_frames) for dev in self.__devs]

        # TODO Round-Robin mode - compute frame_idx

        # If all devices have empty counter list, then empty and returns an empty iterable
        return [] if not all([c.size > 0 for c in counters]) else counters[0]

    def getFrame(self, frame_idx):
        # TODO Round-Robin mode - select receiver that has frame_idx

        frames = [dense_frame.decode(dev.getFrame(frame_idx)) for dev in self.__devs]
        frames = [f for f in frames if f is not None]

        return frames[0] if len(frames) > 0 else None

    def getSparseFrame(self, frame_idx):
        # TODO Round-Robin mode - select receiver that has frame_idx

        frames = [
            sparse_frame.decode(dev.getSparseFrame(frame_idx)) for dev in self.__devs
        ]
        frames = [f for f in frames if f is not None]

        return frames[0] if len(frames) > 0 else None

    def getAccCorrected(self, frame_idx):
        # TODO Round-Robin mode - select receiver that has frame_idx

        frames = [
            dense_frame.decode(dev.getAccCorrected(frame_idx)) for dev in self.__devs
        ]
        frames = [f for f in frames if f is not None]

        return frames[0] if len(frames) > 0 else None

    def getAccPeaks(self, frame_idx):
        # TODO Round-Robin mode - select receiver that has frame_idx

        frames = [dense_frame.decode(dev.getAccPeaks(frame_idx)) for dev in self.__devs]
        frames = [f for f in frames if f is not None]

        return frames[0] if len(frames) > 0 else None
