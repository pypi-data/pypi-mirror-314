# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Utility functions"""


def docstring_from(parent):
    """Inherit the docstring from `parent`, overwriting the current one"""

    def decorated(child):
        child.__doc__ = parent.__doc__
        return child

    return decorated
