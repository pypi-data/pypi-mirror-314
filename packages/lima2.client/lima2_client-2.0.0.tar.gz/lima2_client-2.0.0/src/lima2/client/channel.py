# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

import numpy as np
from abc import ABC, abstractmethod


class Channel(ABC):
    """A base class for channel to retrive data from processing"""

    def __init__(self, name, shape, dtype):
        self._name = name
        self._shape = shape
        self._dtype = dtype

    @abstractmethod
    def progress(self):
        pass

    @abstractmethod
    def __get_item__(self, slice):
        pass

    @abstractmethod
    def __len__(self):
        pass
