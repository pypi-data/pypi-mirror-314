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

from lima2.client.state_machine import State, StateMachine
from lima2.server.timer import Timer


class Proxy:
    """Mock a device proxy of control/receiver device"""

    def __init__(self, instance_name, initial_state=State.IDLE):
        self.__instance_name = instance_name
        self.__state = initial_state
        self.__nb_frames_xferred = 0
        self.__on_end_acq = None
        self.acq_params = None

    @property
    def instance_name(self):
        return self.__instance_name

    @property
    def state(self):
        return self.__state

    @property
    def nb_frames_xferred(self):
        return self.__nb_frames_xferred

    def Prepare(self, uuid):
        assert self.acq_params["nb_frames"] > 0
        assert self.acq_params["expo_time"] > 0.0
        gevent.sleep(1)
        self.__state = State.PREPARED

    def Start(self):
        assert self.__state == State.PREPARED
        assert self.acq_params
        self.__state = State.RUNNING

        def run_acquisition(count):
            print(f"[{self.__instance_name}] acquire frame #{count}")
            self.__nb_frames_xferred = count
            if count == self.acq_params["nb_frames"]:
                self.__state = State.IDLE
                if self.__on_end_acq:
                    self.__on_end_acq(count)

        if self.instance_name != "control":
            # Run acquisition in a gevent.timer
            timer = Timer(
                run_acquisition,
                self.acq_params["expo_time"],
                self.acq_params["nb_frames"],
            )

    def Stop(self):
        if self.__state == State.RUNNING:
            gevent.sleep(1)
            self.__state = State.IDLE

    def Close(self):
        self.__state = State.IDLE

    def fail(self):
        raise RuntimeError("Simulating error")

    def subscribe_event(self, attr_name, evt_type, cbk):
        self.__on_end_acq = cbk

    def unsubscribe_event(self, event_id):
        self.__on_end_acq = None


class Detector:
    def __init__(self):
        self.__devs = [Proxy("control"), Proxy("receiver1"), Proxy("receiver2")]

    @property
    def devs(self):
        return self.__devs

    @property
    def ctrl(self):
        return self.__devs[0]

    @property
    def recvs(self):
        return self.__devs[1:]

    @property
    def states(self):
        return [dev.state for dev in self.__devs]
        # return gevent.joinall([gevent.spawn(dev.state, uuid) for dev in self.__devs])

    @property
    def acq_params(self):
        return [dev.acq_params for dev in self.__devs]

    @acq_params.setter
    def acq_params(self, acq_params):
        for dev in self.__devs:
            dev.acq_params = acq_params


@pytest.fixture
def det():
    det = Detector()
    return det


@pytest.fixture
def fsm(det):
    fsm = StateMachine(det)
    return fsm


def test_initial_state(fsm):
    assert fsm.state == State.UNKNOWN


def test_acquisition(det, fsm):
    TIMEOUT = 10.0

    def test():
        nonlocal det, fsm

        # sync hard
        fsm.state = State.IDLE

        state_history = [fsm.state]
        transition_evt = gevent.event.Event()

        def on_state_change(state):
            print(f"transition from {state_history[-1]} to {state}")
            state_history.append(state)
            transition_evt.set()

        fsm.register_transition_logger(on_state_change)

        uuid_ = uuid.uuid1()
        det.acq_params = {
            "nb_frames": 10,
            "expo_time": 0.01,
        }
        fsm.prepare(uuid_)

        assert transition_evt.wait(TIMEOUT)
        transition_evt.clear()

        assert fsm.state == State.PREPARING

        assert transition_evt.wait(TIMEOUT)
        transition_evt.clear()

        assert fsm.state == State.PREPARED
        assert state_history == [State.IDLE, State.PREPARING, State.PREPARED]
        assert all([state == State.PREPARED for state in det.states])

        fsm.start()

        assert transition_evt.wait(TIMEOUT)
        transition_evt.clear()

        assert fsm.state == State.STARTING

        assert transition_evt.wait(TIMEOUT)
        transition_evt.clear()

        assert fsm.state == State.RUNNING
        assert state_history == [
            State.IDLE,
            State.PREPARING,
            State.PREPARED,
            State.STARTING,
            State.RUNNING,
        ]
        assert all([state == State.RUNNING for state in det.states])

        assert transition_evt.wait(TIMEOUT)
        transition_evt.clear()

        assert fsm.state == State.CLOSING

        assert transition_evt.wait(TIMEOUT)
        transition_evt.clear()

        assert fsm.state == State.IDLE
        assert state_history == [
            State.IDLE,
            State.PREPARING,
            State.PREPARED,
            State.STARTING,
            State.RUNNING,
            State.CLOSING,
            State.IDLE,
        ]
        assert all([state == State.IDLE for state in det.states])

    t = gevent.spawn(test)
    t.join()
