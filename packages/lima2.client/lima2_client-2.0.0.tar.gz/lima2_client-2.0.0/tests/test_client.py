"""Test suite for the Client class (lima2/client/client.py)"""

from uuid import uuid1

import pytest
import tango as tg
import tango.test_context as tc

from lima2.client.client import Client
from lima2.server import Control, Receiver


@pytest.fixture(scope="module")
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
                    "name": "id00/limareceiver/simulator1",
                    "properties": {"log_level": "trace"},
                },
                {
                    "name": "id00/limareceiver/simulator2",
                    "properties": {"log_level": "trace"},
                },
            ],
        },
    ]
    with tc.MultiDeviceTestContext(
        devices_info,
        server_name="lima2",
        instance_name="test",
        process=True,
        green_mode=tg.GreenMode.Gevent,
    ) as context:
        yield context


def patch_properties(dev: tg.DeviceProxy, properties: dict):
    """Replace properties of a DeviceProxy by a dict.

    Without this, tango will systematically raise a tango.NonDbDevice error
    upon calling `dev.get_property()`.
    """
    dev.unfreeze_dynamic_interface()
    dev._properties = properties
    dev.get_property = lambda key: {key: dev._properties[key]}
    dev.freeze_dynamic_interface()


def test_construct_single(server):
    """Construct and use the client with a single receiver"""

    ctrl = server.get_device("id00/limacontrol/simulator")
    recv = server.get_device("id00/limareceiver/simulator1")

    # Required to construct Client
    patch_properties(ctrl, {"receiver_topology": ["single"]})

    c = Client(ctl_dev=ctrl, rcv_devs=[recv])

    curr_acq = c.nb_frames_acquired
    curr_xfer = c.nb_frames_xferred

    ctrl.simulate_acq()
    assert c.nb_frames_acquired.sum == curr_acq.sum + 1

    ctrl.simulate_acq()
    assert c.nb_frames_acquired.sum == curr_acq.sum + 2

    recv.simulate_xfer()
    assert c.nb_frames_xferred.sum == curr_xfer.sum + 1

    recv.simulate_xfer()
    assert c.nb_frames_xferred.sum == curr_xfer.sum + 2


def test_construct_multi(server):
    """Construct and use the client with multiple receivers in a roundrobin topology"""

    ctrl = server.get_device("id00/limacontrol/simulator")
    recv1 = server.get_device("id00/limareceiver/simulator1")
    recv2 = server.get_device("id00/limareceiver/simulator2")

    # Required to construct Client
    patch_properties(ctrl, {"receiver_topology": ["round_robin"]})

    c = Client(ctl_dev=ctrl, rcv_devs=[recv1, recv2])

    curr_acq = c.nb_frames_acquired
    curr_xfer = c.nb_frames_xferred

    # Acq
    ctrl.simulate_acq()
    assert c.nb_frames_acquired.sum == curr_acq.sum + 1

    ctrl.simulate_acq()
    assert c.nb_frames_acquired.sum == curr_acq.sum + 2

    # Xfer on recv1
    recv1.simulate_xfer()
    assert c.nb_frames_xferred.sum == curr_xfer.sum + 1
    assert c.nb_frames_xferred.min == curr_xfer.min
    assert c.nb_frames_xferred.max == curr_xfer.max + 1
    assert c.nb_frames_xferred.avg == curr_xfer.avg + 0.5

    # Xfer on recv2
    recv2.simulate_xfer()
    assert c.nb_frames_xferred.sum == curr_xfer.sum + 2
    assert c.nb_frames_xferred.min == curr_xfer.min + 1
    assert c.nb_frames_xferred.max == curr_xfer.max + 1
    assert c.nb_frames_xferred.avg == curr_xfer.avg + 1


def test_pipeline_current(server, database):
    ctrl = server.get_device("id00/limacontrol/simulator")
    recv1 = server.get_device("id00/limareceiver/simulator1")
    recv2 = server.get_device("id00/limareceiver/simulator2")

    # Required to construct Client
    patch_properties(ctrl, {"receiver_topology": ["round_robin"]})

    c = Client(
        ctl_dev=ctrl,
        rcv_devs=[recv1, recv2],
    )
    # We have not created a pipeline -> calling `current_pipeline` should raise
    with pytest.raises(ValueError):
        _ = c.current_pipeline

    # Create new pipelines, check `Client.pipelines` return value
    uuid_first = uuid1()
    recv1.create_pipeline(str(uuid_first))
    recv2.create_pipeline(str(uuid_first))
    assert c.pipelines == [uuid_first]

    uuid_second = uuid1()
    recv1.create_pipeline(str(uuid_second))
    recv2.create_pipeline(str(uuid_second))
    assert c.pipelines.sort() == [uuid_first, uuid_second].sort()

    # Create pipelines with different uuids on recv1 and recv2
    recv1.create_pipeline(str(uuid1()))
    recv2.create_pipeline(str(uuid1()))

    with pytest.raises(ValueError):
        _ = c.current_pipeline
