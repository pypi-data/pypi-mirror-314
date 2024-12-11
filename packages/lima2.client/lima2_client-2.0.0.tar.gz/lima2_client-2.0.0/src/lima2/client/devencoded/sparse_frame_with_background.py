# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Utility functions to decode Lima data from device server.
"""

import struct
import numpy as np
import typing

from .exception import DevEncodedFormatNotSupported

DATA_HEADER_FORMAT = "<HHIII"
DATA_HEADER_SIZE = struct.calcsize(DATA_HEADER_FORMAT)


class SparseFrameWithBackground(typing.NamedTuple):
    """
    Provide sparse data frame from Lima including few metadata
    """

    index: np.array
    intensity: np.array
    background_avg: np.array
    background_std: np.array

    idx: typing.Optional[int]
    """Index of the frame where 0 is the first frame"""

    def __bool__(self):
        return not self.isEmpty()

    def isEmpty(self):
        return self.index is None

    def densify(self, mask, radius, dummy, normalization=None):
        """Generate a dense image of its sparse representation with background

        :param mask: 2D array with NaNs for mask and pixel radius for the valid pixels
        :param radius: 1D array with the radial distance
        :param dummy: numerical value for masked-out pixels in dense image
        :param normalization: flat*solidangle*polarization*... array
        :return dense array
        """
        dense = np.interp(mask, radius, self.background_avg)
        if self.background_std is not None:
            std = np.interp(mask, radius, self.background_std)
            np.maximum(0.0, np.random.normal(dense, std), out=dense)
        if normalization is not None:
            dense *= normalization

        flat = dense.ravel()
        flat[self.index] = self.intensity
        dtype = self.intensity.dtype
        if np.issubdtype(dtype, np.integer):
            dense = np.round(dense)
        dense = np.ascontiguousarray(dense, dtype=dtype)
        dense[np.logical_not(np.isfinite(mask))] = dummy
        return dense

    def densify_peaks(self, shape):
        """Generate a dense image of its sparse representation with peaks only

        :param mask: 2D array with NaNs for mask and pixel radius for the valid pixels
        :return dense array
        """
        dense = np.zeros(shape, self.intensity.dtype)
        flat = dense.ravel()
        flat[self.index] = self.intensity
        return dense


def decode_sparse_frame(raw_data: bytes) -> SparseFrameWithBackground:
    """Decode data provided by Lima2

    Argument:
        raw_data: DevEncoded data

    Returns:
        A SparseFrameWithBackground.
    """

    if isinstance(raw_data, tuple):
        # Support the direct output from proxy.readImage
        if raw_data[0] != "SPARSE_FRAME_WITH_BACKGROUND":
            raise DevEncodedFormatNotSupported(
                "Data type SPARSE_FRAME expected (found %s)." % raw_data[0]
            )
        raw_data = raw_data[1]

    (
        width,
        height,
        nb_bins,
        nb_peaks,
        frame_idx,
    ) = struct.unpack_from(DATA_HEADER_FORMAT, raw_data)

    offset = DATA_HEADER_SIZE
    index = np.frombuffer(raw_data, count=nb_peaks, offset=offset, dtype=np.int32)
    offset += index.nbytes
    intensity = np.frombuffer(raw_data, count=nb_peaks, offset=offset, dtype=np.float32)
    offset += intensity.nbytes
    background_avg = np.frombuffer(
        raw_data, count=nb_bins, offset=offset, dtype=np.float32
    )
    offset += background_avg.nbytes
    background_std = np.frombuffer(
        raw_data, count=nb_bins, offset=offset, dtype=np.float32
    )

    return SparseFrameWithBackground(
        index, intensity, background_avg, background_std, frame_idx
    )
