# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

import gevent
from lima2.server.timer import Timer

hub = gevent.get_hub()


def test_timer():
    last_count = 0

    def callback(count):
        nonlocal last_count
        last_count = count

    timer = Timer(callback, 0.01, 10)

    hub.join()

    assert last_count == 10
