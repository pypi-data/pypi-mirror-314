# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Finite state machine definition for the detector.
"""

import logging
from enum import Enum, auto
import gevent

import finite_state_machine as fsm
from finite_state_machine import transition

from tango import EventType

# Create a logger
_logger = logging.getLogger(__name__)


class State(Enum):
    """The possible states of the Detector state machine."""

    # Enum values for '<enum 'State'>' must start at 0 and increment by 1.
    IDLE = 0
    PREPARING = auto()
    PREPARED = auto()
    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    ENDING = auto()
    CLOSING = auto()
    RESETTING = auto()
    FAULT = auto()
    UNKNOWN = auto()


# Conditions
def trigger_mode_software(fsm):
    # TODO
    return True


class StateMachine(fsm.StateMachine):
    """Detector Finite State Machine."""

    def __init__(self, det, timeout=None):
        """
        Construct a StateMachine that control the state of the detector.

        Args:
            det: A Detector object
            timeout: If given, specifies a maximum number of seconds to wait.

        """
        self._state = State.UNKNOWN
        self.__det = det
        self.__loggers = []
        super().__init__()

        def on_acq_state_change(evt):
            # Filter spurious error events (if the device is restarted)
            if evt.err:
                _logger.info(f"on_acq_state_change got an error event {evt.errors}")
                return

            AcqState = type(evt.device.acq_state)
            acq_state = AcqState(evt.attr_value.value)
            _logger.debug(f"on_acq_state {acq_state}")

            # TODO Check the global state of the detector according to the individual states
            if acq_state == AcqState.fault and self._state not in [
                State.FAULT,
                State.UNKNOWN,
            ]:
                self.error()

        self.event_ids = {
            r: r.subscribe_event(
                "acq_state",
                EventType.CHANGE_EVENT,
                on_acq_state_change,
            )
            for r in self.__det.devs
        }

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state != value:
            self._state = value
            self.on_state_change(value)

    @transition(
        source=[State.IDLE, State.PREPARED, State.FAULT],
        target=State.PREPARING,
        on_error=State.IDLE,
    )
    def prepare(self, uuid: str):
        def prepare():
            greenlets = [gevent.spawn(dev.Prepare, uuid) for dev in self.__det.devs]
            gevent.joinall(greenlets, raise_error=True)

        greenlet = gevent.spawn(prepare)
        greenlet.link(self.prepare_end)
        return greenlet

    @transition(source=State.PREPARING, target=State.PREPARED, on_error=State.IDLE)
    def prepare_end(self, greenlet):
        greenlet.get()

    @transition(source=State.PREPARED, target=State.STARTING, on_error=State.FAULT)
    def start(self):
        def start():
            greenlets = [gevent.spawn(dev.Start) for dev in self.__det.devs]
            gevent.joinall(greenlets, raise_error=True)

        self.__subscribe_events()
        greenlet = gevent.spawn(start)
        greenlet.link(self.start_end)
        return greenlet

    @transition(source=State.STARTING, target=State.RUNNING)
    def start_end(self, greenlet):
        greenlet.get()

    @transition(
        source=State.RUNNING, target=State.RUNNING, conditions=[trigger_mode_software]
    )
    def trigger(self):
        greenlet = gevent.spawn(self.__det.ctrl.Trigger)
        greenlet.join()

    @transition(source=State.RUNNING, target=State.RUNNING)
    def trigger_end(self):
        pass

    @transition(source=State.RUNNING, target=State.STOPPING)
    def stop(self):
        def stop():
            greenlets = [gevent.spawn(dev.Stop) for dev in self.__det.devs]
            gevent.joinall(greenlets, raise_error=True)

        greenlet = gevent.spawn(stop)
        greenlet.link(self.stop_end)
        return greenlet

    @transition(source=State.STOPPING, target=State.CLOSING)
    def stop_end(self, greenlet):
        greenlet.get()

        # Send close to control device only (recv close by themselves)
        greenlet = gevent.spawn(self.__det.ctrl.Close)
        greenlet.link(self.close_end)

    @transition(source=State.RUNNING, target=State.CLOSING)
    def close(self):
        # Send close to control device only (recv close by themselves)
        greenlet = gevent.spawn(self.__det.ctrl.Close)
        greenlet.link(self.close_end)

    @transition(source=State.CLOSING, target=State.IDLE)
    def close_end(self, greenlet):
        greenlet.get()

    @transition(source=State.FAULT, target=State.IDLE)
    def reset_acq(self):
        greenlets = [gevent.spawn(dev.Reset) for dev in self.__det.devs]
        gevent.joinall(greenlets, raise_error=True)

    @transition(source=State.CLOSING, target=State.IDLE)
    def acq_end(self):
        self.__unsubscribe_events()

    @transition(
        source=[
            State.IDLE,
            State.PREPARING,
            State.STARTING,
            State.RUNNING,
            State.STOPPING,
            State.ENDING,
        ],
        target=State.FAULT,
    )
    def error(self):
        # Send close to control device only (recv close by themselves)
        self.__det.ctrl.Close()

    def __subscribe_events(self):
        nb_receivers = len(self.__det.recvs)
        nb_frames_xferreds = []
        event_ids = {}

        def on_end_acq(evt):
            nonlocal nb_frames_xferreds
            nonlocal event_ids

            # Filter spurious error events (if the device is restarted)
            if evt.err:
                _logger.info(f"on_end_acq got an error event {evt.errors}")
                return

            nb_frames_xferreds.append(evt)

            if len(nb_frames_xferreds) == nb_receivers:
                for r, e in event_ids.items():
                    r.unsubscribe_event(e)

                _logger.debug(f"on_end_acq while {self.state}")
                self.close()

                nb_frames_xferreds = []

        event_ids = {
            r: r.subscribe_event(
                "nb_frames_xferred",
                EventType.DATA_READY_EVENT,
                on_end_acq,
            )
            for r in self.__det.recvs
        }

    def register_transition_logger(self, logger):
        """
        Register a logger to be notified on transition.

        Args:
            logger: A callback with the following signature.

        Example:
            def on_transition(source, target):
                print(f"transition from {source} to {target}")

            fsm.register_transition_logger(on_transition)
        """
        self.__loggers.append(logger)

    def unregister_transition_logger(self, logger):
        """
        Unregister a given transition logger function.

        Args:
            logger: A callback to unregister.
        """
        if logger in self.__loggers:
            self.__loggers.remove(logger)

    def on_state_change(self, state):
        _logger.debug(f"on_state_change {state}")
        greenlets = [gevent.spawn(logger, state) for logger in self.__loggers]
        gevent.joinall(greenlets, raise_error=True)
