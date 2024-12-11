# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Processing base class.

An instance of Processing represents one processing pipeline, possibly distributed across multiple
Lima2 receivers. It has knowledge of the topology, and therefore can provide aggregated progress
counters during/after an acquisition.
"""
from __future__ import annotations

import json
import logging
from uuid import UUID

import tango
from beartype import beartype
from jsonschema_default import create_from

from .aggregator import (
    Aggregator,
    ProgressCounter,
    SingleCounter,
    Topology,
)
from .convert import frame_info_to_shape_dtype

# Create a logger
_logger = logging.getLogger(__name__)


class ProcessingMetaclass(type):
    def __init__(self, name, bases, namespace, **kwargs):
        self.tango_db = None
        if "tango_class" in kwargs:
            self.tango_class = kwargs["tango_class"]

    @property
    def params_schema(self) -> dict:
        """
        Get the parameters's schema for the given tango_class
        """
        if not self.tango_db:
            self.tango_db = tango.Database()

        def get_schema(param: str) -> dict:
            prop = self.tango_db.get_class_attribute_property(self.tango_class, param)
            # Each attribute property is a StdStringVector with a single value
            try:
                schema_json = prop[param]["schema"][0]
            except KeyError as e:
                raise ValueError(
                    f"Schema for '{param}' not found for processing class '{self.tango_class}'"
                ) from e
            return json.loads(schema_json)

        return get_schema("proc_params")

    @property
    def params_default(self) -> dict:
        """
        Returns a set of parameters with default values.
        """
        return create_from(self.params_schema)


@beartype
class Processing(object, metaclass=ProcessingMetaclass):
    """A base class for all processings."""

    DEFAULT_TANGO_TIMEOUT = 20 * 60  #

    def __init__(
        self,
        uuid: UUID,
        proc_urls: list[str],
        topology: Topology,
        timeout: int = DEFAULT_TANGO_TIMEOUT,
    ):
        """Construct a Processing object.

        Args:
            uuid: Unique identifer of the acquisition
            proc_urls: Variable length processing device instance names (aka domain/family/member)

        """
        # Preconditions
        if not proc_urls:
            raise ValueError("Must provide at least one processing")

        self.__uuid = uuid
        self.__devs = [tango.DeviceProxy(url) for url in proc_urls]

        for d in self.__devs:
            d.set_green_mode(tango.GreenMode.Gevent)
            d.set_timeout_millis(timeout * 1000)

        self.aggregator = Aggregator.from_topology(topology=topology)

    @property
    def uuid(self):
        """Return the UUID of the processing"""
        return self.__uuid

    @property
    def input_frame_info(self):
        """Return the dtype and shape of the input frame for each receivers"""
        return [
            frame_info_to_shape_dtype(json.loads(dev.input_frame_info))
            for dev in self.__devs
        ]

    @property
    def processed_frame_info(self):
        """Return the dtype and shape of the processed frame for each receivers"""
        return [
            frame_info_to_shape_dtype(json.loads(dev.processed_frame_info))
            for dev in self.__devs
        ]

    @property
    def progress_counters(self) -> list[ProgressCounter]:
        """Get the list of aggregated progress counters"""
        pcs_by_rcv = [json.loads(dev.progress_counters) for dev in self.__devs]

        # Set of unique progress counter names
        pc_keys = set()
        for rcv_pcs in pcs_by_rcv:
            for k in rcv_pcs.keys():
                pc_keys.add(k)

        # Sanity check: all receivers have the same progress counters (assume homogeneous)
        # Perhaps not true in all future topologies
        for rcv in pcs_by_rcv:
            for key in pc_keys:
                assert key in rcv.keys()

        aggregated_pcs: list[ProgressCounter] = []
        for pc_key in pc_keys:
            single_counters = []
            for dev, pcs in zip(self.__devs, pcs_by_rcv):
                single_counters.append(
                    SingleCounter(name=pc_key, value=pcs[pc_key], source=dev.name())
                )

            aggregated_pcs.append(self.aggregator(single_counters=single_counters))

        return aggregated_pcs

    def ping(self):
        """
        Ping all the devices of the system.

        Raises:
            tango.ConnectionFailed: if the connection failed.

        """
        for d in self.__devs:
            d.ping()

    @property
    def is_finished(self):
        """A list of `is_finished` for each devices."""
        return [dev.is_finished for dev in self.__devs]

    def register_on_finished(self, cbk):
        """
        Register a callback function to be notified on pipeline finish

        Arg:
            cbk: A callback `on_finished(evt: Tango.Event)` called for each receivers

        Returns:
            A dict mapping the processing instance name with the event id
        """

        return {
            proc: proc.subscribe_event(
                "is_finished", tango.EventType.DATA_READY_EVENT, cbk
            )
            for proc in self.__devs
        }

    @property
    def last_error(self):
        """A list of `last_error` for each devices."""
        return [dev.last_error for dev in self.__devs]

    def register_on_error(self, cbk):
        """
        Register a callback function to be notified on pipeline error

        Arg:
            cbk: A callback `on_error(evt: Tango.Event)` called for each receivers

        Returns:
            A dict mapping the processing instance name with the event id
        """

        return {
            proc: proc.subscribe_event(
                "last_error", tango.EventType.DATA_READY_EVENT, cbk
            )
            for proc in self.__devs
        }

    def __repr__(self) -> str:
        return "\n".join([f" - {counter}" for counter in self.progress_counters])
