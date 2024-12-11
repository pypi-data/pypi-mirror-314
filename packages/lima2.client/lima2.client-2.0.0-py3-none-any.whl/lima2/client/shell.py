#!/usr/bin/env python

"""Lima2 client interactive shell

Given a Tango server at $TANGO_HOST and the l2c_config.yaml file, launch an ipython interactive
shell with a Client object initialized and some example control/acquisition/processing parameters.
"""

# Apply gevent monkeypatch before any other imports
# This enables async actions to run in the background (e.g. state machine)
import gevent.monkey

gevent.monkey.patch_all(thread=False)

from typing import Literal
from beartype import beartype
from functools import partial
from uuid import uuid1
from lima2.client.client import Client
import tango


@beartype
def get_proc_params(pipeline: Literal["Legacy", "Smx", "Xpcs"]) -> dict:
    """Get the default processing params for a pipeline"""
    from . import pipelines

    proc_class = pipelines.get_class(f"LimaProcessing{pipeline}")
    proc_params = proc_class.params_default
    proc_params["class_name"] = proc_class.tango_class

    return proc_params


def run_acquisition(
    c: Client,
    ctl_params: dict,
    rcv_params: list,
    proc_params: list,
    nb_frames: int,
    expo_time: float,
    latency_time: float,
    trigger_mode: str = "internal",
):
    ctl_params["acq"]["trigger_mode"] = "internal"
    ctl_params["acq"]["nb_frames"] = nb_frames
    for p in rcv_params:
        p["acq"]["nb_frames"] = nb_frames / len(rcv_params)
    ctl_params["acq"]["expo_time"] = int(expo_time * 1e6)
    for p in rcv_params:
        p["acq"]["expo_time"] = int(expo_time * 1e6)
    ctl_params["acq"]["latency_time"] = int(latency_time * 1e6)
    for p in rcv_params:
        p["acq"]["latency_time"] = int(latency_time * 1e6)
    for p in proc_params:
        p["saving"]["nb_frames_per_file"] = 10
        p["saving"]["file_exists_policy"] = "overwrite"

    # round robin
    for i, p in enumerate(rcv_params):
        p["xfer"]["slice"]["start"] = i
        p["xfer"]["slice"]["stride"] = len(rcv_params)

    c.detector.prepare_acq(uuid1(), ctl_params, rcv_params, proc_params)
    c.detector.start_acq()


def main():
    import copy
    import os

    import tango as tg

    try:
        from IPython import start_ipython
    except ImportError as e:
        raise ImportError(
            f"Dependency '{e.name}' not found. To fix:\n"
            "$ pip install lima2-client[shell]"
        ) from e

    from traitlets.config import Config

    import lima2.client as l2c

    if not os.getenv("TANGO_HOST"):
        raise ValueError("TANGO_HOST must be exported")

    #############
    # Populate user namespace

    config_filename = "l2c_config.yaml"
    try:
        c = Client.from_yaml(config_filename=config_filename)
    except tango.ConnectionFailed as e:
        raise RuntimeError(
            f"Could not establish a connection to the Tango server at {os.getenv('TANGO_HOST')}."
        ) from e
    except tango.DevFailed as e:
        raise RuntimeError(
            f"Device connection failed. Please check your configuration in '{config_filename}'.\n"
            "See error above for details."
        ) from e

    # Some sensible default parameters
    proc_params = get_proc_params("Legacy")

    ctl_params = c.detector.params_default[c.detector.ctrl.name()]["acq_params"]

    rcv_params = [copy.deepcopy(ctl_params) for _ in range(len(c.detector.recvs))]

    proc_params = [copy.deepcopy(proc_params) for _ in range(len(c.detector.recvs))]
    for i, p in enumerate(proc_params):
        p["saving"]["file_exists_policy"] = "overwrite"
        # TODO(mdu) should be unnecessary when mpi rank is properly used server-side
        p["saving"]["filename_prefix"] = f"lima2_rcv_{i}"

    user_namespace = {
        "tg": tg,
        "l2c": l2c,
        "c": c,
        "get_proc_params": get_proc_params,
        "uuid1": uuid1,
        "ctl_params": ctl_params,
        "rcv_params": rcv_params,
        "proc_params": proc_params,
        "run_acquisition": partial(
            run_acquisition, c, ctl_params, rcv_params, proc_params
        ),
    }

    #############
    # IPython config
    config = Config()

    # Show defined symbols on ipython banner
    config.TerminalInteractiveShell.banner2 = (
        "\n"
        "===============\n"
        "| Lima2 shell |\n"
        "===============\n\n"
        f"Defined symbols: {[key for key in user_namespace]}\n"
        "Run an acquisition as follows:\n"
        " c.detector.prepare_acq(uuid1(), ctl_params, rcv_params, proc_params)\n"
        " c.detector.start_acq()\n"
    )

    # Enable autoreload
    config.InteractiveShellApp.extensions = ["autoreload"]
    config.InteractiveShellApp.exec_lines = [r"%autoreload all"]

    start_ipython(argv=[], user_ns=user_namespace, config=config)


if __name__ == "__main__":
    import sys

    sys.exit(main())
