# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""User-facing interface exposing Lima2's control and acquisition API.

The role of the client is to connect the user to the Lima2 devices via Tango.

The Client object instantiates a `Detector` object, allowing the user to control the acquisition
via the standard prepare/start/stop sequence.

The client hides away the topology by providing aggregated stats and counters in the form of
`ProgressCounter` objects. If needed, these can be explored to trace the information back to
individual receivers, for instance if one of them is stuck on a frame while the rest are still
processing data.
"""

from uuid import UUID

import tango as tg
import yaml
from beartype import beartype
from typing_extensions import Optional, Self

from . import pipelines, state_machine
from .aggregator import Aggregator, ProgressCounter, SingleCounter
from .detector import Detector
from .processing import Processing, Topology
from .utils import docstring_from


@beartype
class Client:
    """Lima2 user-facing client."""

    def __init__(
        self,
        ctl_dev: tg.DeviceProxy,
        rcv_devs: list[tg.DeviceProxy],
    ):
        """Construct a Client given tango device proxies.

        The Client can also be built from a yaml config file (see `from_yaml`).
        The topology is queried from the control device properties.
        """

        self.detector = Detector(ctl_dev, *rcv_devs)

        try:
            topology_prop = ctl_dev.get_property("receiver_topology")
            topology_name = topology_prop["receiver_topology"][0]
            self.topology = Topology(topology_name)
        except IndexError:
            # Property does not exist
            raise RuntimeError(
                "Could not find 'receiver_topology' property in control device"
            )
        except ValueError as e:
            # Invalid topology (no matching name in Topology enum)
            raise ValueError(
                f"No matching topology type for {repr(topology_name)}"
            ) from e

        self.recv_devs = rcv_devs
        self.aggregator = Aggregator.from_topology(self.topology)

        # Cache of processing pipelines by uuid (see method `pipeline`)
        self.__pipelines: dict[UUID, Processing] = {}

        self.tango_db = tg.Database()

    @classmethod
    def from_yaml(
        cls,
        config_filename: str = "l2c_config.yaml",
    ) -> Self:
        with open(config_filename) as config_f:
            # Raises on io/parsing error
            config = yaml.safe_load(config_f)

        ctl_url = config["ctl_url"]
        rcv_urls = config["rcv_urls"]

        ctl_dev = tg.DeviceProxy(ctl_url)
        rcv_devs = [tg.DeviceProxy(url) for url in rcv_urls]

        return Client(ctl_dev=ctl_dev, rcv_devs=rcv_devs)

    ####################################################################################
    # Client properties
    ####################################################################################

    @property
    def nb_recvs(self):
        return len(self.recv_devs)

    ####################################################################################
    # Detector properties
    ####################################################################################

    @property
    @docstring_from(Detector.det_info)
    def det_info(self):
        return self.detector.det_info

    @property
    @docstring_from(Detector.det_status)
    def det_status(self):
        return self.detector.det_status

    @property
    @docstring_from(Detector.det_capabilities)
    def det_capabilities(self):
        return self.detector.det_capabilities

    @property
    @docstring_from(Detector.state)
    def state(self) -> state_machine.State:
        return self.detector.state

    @property
    @docstring_from(Detector.params_default)
    def params_default(self) -> dict:
        return self.detector.params_default

    ####################################################################################
    # Control
    ####################################################################################

    @docstring_from(Detector.prepare_acq)
    def prepare_acq(self, *args, **kwargs):
        self.detector.prepare_acq(*args, **kwargs)

    @docstring_from(Detector.start_acq)
    def start_acq(self):
        self.detector.start_acq()

    @docstring_from(Detector.trigger)
    def trigger(self):
        self.detector.trigger()

    @docstring_from(Detector.stop_acq)
    def stop_acq(self):
        self.detector.stop_acq()

    @docstring_from(Detector.reset_acq)
    def reset_acq(self):
        self.detector.reset_acq()

    ####################################################################################
    # Progress counters
    ####################################################################################

    @property
    def nb_frames_acquired(self) -> ProgressCounter:
        """Number of frames acquired"""
        return ProgressCounter.from_single(
            SingleCounter(
                name="nb_frames_acquired",
                value=self.detector.nb_frames_acquired,
                source=self.detector.ctrl.name(),
            )
        )

    @property
    def nb_frames_xferred(self) -> ProgressCounter:
        """Aggregated number of frames transferred"""
        return self.aggregator(
            [
                SingleCounter(
                    name="nb_frames_xferred",
                    value=recv.nb_frames_xferred,
                    source=recv.name(),
                )
                for recv in self.detector.recvs
            ]
        )

    ####################################################################################
    # Pipelines
    ####################################################################################

    @property
    def pipelines(self) -> list[UUID]:
        """Get list of available pipelines UUID"""
        uuids = [recv.pipelines for recv in self.recv_devs]
        if all(uuid is None for uuid in uuids):
            return []
        return [UUID(u) for u in {y for x in uuids for y in x}]

    def pipeline(self, uuid: Optional[UUID] = None) -> Optional[Processing]:
        """Get a specific pipeline by uuid. Return the current one by default (uuid=None)"""
        if uuid is None:
            return self.current_pipeline

        if uuid in self.__pipelines:
            return self.__pipelines[uuid]

        # uuid isn't in the local cache of pipelines: get it from Tango
        instances = self.tango_db.get_device_exported(f"*/limaprocessing/{uuid}*")
        if not instances:
            raise ValueError(f"Pipeline not found in tango database: {uuid=}")

        class_names = [
            self.tango_db.get_device_info(instance).class_name for instance in instances
        ]

        # Select the processing according to the Tango class (Homogeneous processing for now)
        pipeline_class = pipelines.get_class(tango_class_name=class_names[0])

        # Instantiate pipeline
        self.__pipelines[uuid] = pipeline_class(uuid, list(instances), self.topology)

        return self.__pipelines[uuid]

    @property
    def current_pipeline(self) -> Optional[Processing]:
        uuids: list[str] = [recv.current_pipeline for recv in self.recv_devs]

        if all([uuid == "" for uuid in uuids]):
            raise ValueError("No pipeline present in the tango database")

        uuids: list[UUID] = [UUID(uuid) for uuid in uuids]

        if not all([uuid == uuids[0] for uuid in uuids]):
            raise ValueError(f"Inconsistent pipeline uuids on all receivers: {uuids=}")

        return self.pipeline(uuids[0])

    def erase_pipeline(self, uuid: UUID):
        """Erase a pipeline instance"""
        self.__pipelines.pop(uuid, None)
        for recv in self.recv_devs:
            recv.erasePipeline(str(uuid))

    ####################################################################################
    # Utility
    ####################################################################################

    def __repr__(self) -> str:
        return "\n".join(
            [
                "Lima2 client",
                f"State: {self.detector.state}",
                "Controller:",
                f" {self.detector.ctrl}",
                f"Receivers ({self.topology}):",
                *[f" - {recv}" for recv in self.detector.recvs],
                "Progress counters:",
                f" - {self.nb_frames_acquired}",
                f" - {self.nb_frames_xferred}",
                str(self.current_pipeline) if self.__pipelines else "",
            ]
        )
