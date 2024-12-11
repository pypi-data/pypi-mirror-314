# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Aggregators for different receiver topologies (single, round-robin, etc).

An aggregator class defines a `__call__` method which takes a list of `SingleCounters` as
parameter. Its purpose is to turn this list into an aggregated `ProgressCounter` according
to the topology of Lima2 receivers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from statistics import mean

from beartype import beartype
from typing_extensions import Self, Union


class Topology(Enum):
    """Receiver topology

    Values must match lima2's corresponding receiver_topology enum.
    """

    SINGLE = "single"
    ROUND_ROBIN = "round_robin"


@dataclass
class SingleCounter:
    """Progress counter reported by a single receiver.

    The Client is reponsible for aggregating SingleCounters into a ProgressCounter."""

    # Counter label (e.g. nb_frames_acquired)
    name: str
    value: int
    # Holds the name of the device that generated this counter
    source: str


@beartype
@dataclass
class ProgressCounter:
    """Final progress counter after aggregation of one or more SingleCounters by an Aggregator."""

    name: str
    counters: list[SingleCounter]

    @classmethod
    def from_single(cls, single_counter: SingleCounter) -> Self:
        """Construct from a single SingleCounter"""
        return ProgressCounter(name=single_counter.name, counters=[single_counter])

    @property
    def sum(self) -> int:
        return sum([c.value for c in self.counters])

    @property
    def max(self) -> int:
        return max([c.value for c in self.counters])

    @property
    def min(self) -> int:
        return min([c.value for c in self.counters])

    @property
    def avg(self) -> Union[int, float]:
        return mean([c.value for c in self.counters])

    def __repr__(self) -> str:
        return f"{self.name}: {self.sum}/{self.min}/{self.max}/{self.avg} (total/min/max/avg)"


@beartype
class Aggregator(ABC):
    """Aggregator base"""

    @abstractmethod
    def __call__(self, single_counters: list[SingleCounter]) -> ProgressCounter:
        pass

    @classmethod
    def from_topology(cls, topology: Topology) -> Self:
        """Instantiate an aggregator given a topology"""
        if topology == Topology.SINGLE:
            return SingleAggregator()
        elif topology == Topology.ROUND_ROBIN:
            return RoundRobinAggregator()
        raise NotImplementedError(f"Case not covered for {topology=}")


@beartype
class SingleAggregator(Aggregator):
    """Aggregator for a single-receiver topology."""

    def __call__(self, single_counters: list[SingleCounter]) -> ProgressCounter:
        # Single-counter topology -> expect one value
        assert (
            len(single_counters) == 1
        ), f"Expected one value in SingleAggregator but got {single_counters=}"

        pc = ProgressCounter.from_single(single_counters[0])
        return pc


@beartype
class RoundRobinAggregator(Aggregator):
    """Aggregator for a multi-receiver round-robin topology."""

    def __call__(self, single_counters: list[SingleCounter]) -> ProgressCounter:
        # Multi-receiver topology -> expect more than 1 value
        assert (
            len(single_counters) > 1
        ), f"Expected more than one value in RoundRobinAggregator but got {single_counters=}"

        name = single_counters[0].name
        return ProgressCounter(
            name=name,
            counters=single_counters,
        )
