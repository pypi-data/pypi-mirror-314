# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Convertion routines.

Frame info is serialized as {'dimensions': {'x': 2068, 'y': 512}, 'nb_channels': 2, 'pixel_type': 'gray16'}
"""

import numpy as np


def pixel_type_to_np_dtype(pixel_type):
    """convert from pixel enum type to numpy type"""
    if pixel_type == "gray8s":
        return np.int8
    elif pixel_type == "gray8":
        return np.uint8
    elif pixel_type == "gray16s":
        return np.int16
    elif pixel_type == "gray16":
        return np.uint16
    elif pixel_type == "gray32s":
        return np.int32
    elif pixel_type == "gray32":
        return np.uint32
    elif pixel_type == "gray32f":
        return np.float32
    elif pixel_type == "gray64f":
        return np.float64
    else:
        raise RuntimeError(f"Unsupported pixel type '{pixel_type}'")


def frame_info_to_shape_dtype(frame_info):
    return dict(
        shape=(
            frame_info["nb_channels"],
            frame_info["dimensions"]["y"],
            frame_info["dimensions"]["x"],
        ),
        dtype=pixel_type_to_np_dtype(frame_info["pixel_type"]),
    )
