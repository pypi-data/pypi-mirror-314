"""Test suite for Aggregator classes (lima2/client/aggregator.py)"""

import pytest
from lima2.client.aggregator import (
    SingleCounter,
    SingleAggregator,
    RoundRobinAggregator,
)


#######################################
# Single receiver


@pytest.fixture
def single_aggregator():
    return SingleAggregator()


def test_single_aggregator(single_aggregator):
    """Nominal case"""
    single_counters = [
        SingleCounter(name="my_counter", value=42, source="id00/some/device")
    ]

    progress_counter = single_aggregator(single_counters=single_counters)

    assert progress_counter.name == "my_counter"
    assert progress_counter.sum == 42
    assert progress_counter.min == 42
    assert progress_counter.max == 42
    assert progress_counter.avg == 42


def test_single_aggregator_multiple_values(single_aggregator):
    """Single aggregator cannot handle multiple counter values (as in multi-receiver topology)"""
    single_counters = [
        SingleCounter(name="my_counter", value=42, source="id00/some/device"),
        SingleCounter(name="my_counter", value=43, source="id00/some/device"),
    ]

    with pytest.raises(AssertionError):
        _ = single_aggregator(single_counters=single_counters)


#######################################
# Round robin


@pytest.fixture
def rr_aggregator():
    return RoundRobinAggregator()


def test_rr_aggregator_multiple_values(rr_aggregator):
    """Nominal case"""
    single_counters = [
        SingleCounter(name="my_counter", value=42, source="id00/some/device"),
        SingleCounter(name="also_my_counter", value=43, source="id00/some/device"),
    ]

    progress_counter = rr_aggregator(single_counters=single_counters)

    assert progress_counter.name == "my_counter"
    assert progress_counter.sum == 42 + 43
    assert progress_counter.min == 42
    assert progress_counter.max == 43
    assert progress_counter.avg == (42 + 43) / 2


def test_rr_aggregator_single_value(rr_aggregator):
    """Round robin aggregator isn't expected to handle a single value"""
    single_counters = [
        SingleCounter(name="my_counter", value=42, source="id00/some/device"),
    ]

    with pytest.raises(AssertionError):
        _ = rr_aggregator(single_counters=single_counters)
