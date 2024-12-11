# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

import pytest
import gevent
import gevent.event
import uuid

from lima2.client.detector import Detector
from lima2.client import State
from lima2.server import Control, Receiver

from tango import DevState, GreenMode
from tango.test_context import MultiDeviceTestContext


@pytest.fixture
def server(database):
    devices_info = [
        {
            "class": Control,
            "devices": [
                {
                    "name": "id00/limacontrol/simulator",
                    "properties": {"log_level": "trace"},
                }
            ],
        },
        {
            "class": Receiver,
            "devices": [
                {
                    "name": "id00/limareceiver/simulator",
                    "properties": {"log_level": "trace"},
                }
            ],
        },
    ]
    with MultiDeviceTestContext(
        devices_info,
        server_name="lima2",
        instance_name="test",
        # db="simulator.db",
        process=True,
        green_mode=GreenMode.Gevent,
    ) as context:
        yield context


def test_aquisition(server):
    TIMEOUT = 10.0

    ctrl = server.get_device("id00/limacontrol/simulator")
    recv = server.get_device("id00/limareceiver/simulator")

    # recv.get_green_mode()

    assert ctrl.State() == DevState.ON
    assert recv.State() == DevState.ON

    det = Detector(ctrl, recv)

    assert det.state == State.IDLE

    state_history = [det.state]
    transition_evt = gevent.event.Event()

    def on_state_change(state):
        print(f"transition from {state_history[-1]} to {state}")
        state_history.append(state)
        transition_evt.set()

    det.register_transition_logger(on_state_change)

    uuid_ = uuid.uuid1()
    ctrl_params = {
        "nb_frames": 10,
        "expo_time": 0.01,
    }
    acq_params = {
        "nb_frames": 10,
        "expo_time": 0.01,
    }
    proc_params = {}
    det.prepare_acq(uuid_, ctrl_params, [acq_params], [proc_params])

    assert transition_evt.wait(TIMEOUT)
    transition_evt.clear()

    assert det.state == State.PREPARING

    assert transition_evt.wait(TIMEOUT)
    transition_evt.clear()

    assert det.state == State.PREPARED
    assert state_history == [State.IDLE, State.PREPARING, State.PREPARED]
    assert all([state == state.PREPARED for state in det.dev_states])

    det.start_acq()

    assert transition_evt.wait(TIMEOUT)
    transition_evt.clear()

    assert det.state == State.STARTING

    assert transition_evt.wait(TIMEOUT)
    transition_evt.clear()

    assert det.state == State.RUNNING
    assert state_history == [
        State.IDLE,
        State.PREPARING,
        State.PREPARED,
        State.STARTING,
        State.RUNNING,
    ]
    assert all([state == state.RUNNING for state in det.dev_states])

    assert transition_evt.wait(TIMEOUT)
    transition_evt.clear()

    assert det.state == State.CLOSING

    assert transition_evt.wait(TIMEOUT)
    transition_evt.clear()

    assert det.state == State.IDLE
    assert state_history == [
        State.IDLE,
        State.PREPARING,
        State.PREPARED,
        State.STARTING,
        State.RUNNING,
        State.CLOSING,
        State.IDLE,
    ]
    assert all([state == state.IDLE for state in det.dev_states])
    assert det.nb_frames_acquired == ctrl_params["nb_frames"]
    assert det.nb_frames_xferred == [acq_params["nb_frames"]]


def test_processing(server):
    TIMEOUT = 10.0

    ctrl = server.get_device("id00/limacontrol/simulator")
    recv = server.get_device("id00/limareceiver/simulator")

    # recv.get_green_mode()

    assert ctrl.State() == DevState.ON
    assert recv.State() == DevState.ON

    det = Detector(ctrl, recv)

    uuid_ = uuid.uuid1()
    ctrl_params = {
        "nb_frames": 10,
        "expo_time": 0.01,
    }
    acq_params = {
        "nb_frames": 10,
        "expo_time": 0.01,
    }
    proc_params = {}
    det.prepare_acq(uuid_, ctrl_params, [acq_params], [proc_params])

    proc = det.get_processing(uuid_)
