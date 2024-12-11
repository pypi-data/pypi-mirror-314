# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Pipelines package

This package contains a module for each supported processing pipeline.

This file loads each module and adds its respective Processing class to a dictionary,
allowing other modules to find pipeline classes by tango class name, e.g:

```
legacy_class = pipelines.get_class("LimaProcessingLegacy")
legacy_pipeline = legacy_class(...)
```
"""

import importlib
import os
import pkgutil
from typing import Type

_pipeline_modules = []
for module_info in pkgutil.iter_modules(path=[os.path.dirname(__file__)]):
    # Skip subpackages
    if module_info.ispkg:
        continue

    _pipeline_modules.append(
        importlib.import_module(f"{__package__}.{module_info.name}")
    )

# Holds pairs of (pipeline_name, pipeline_class)
by_name: dict[str, Type] = {
    mod.Processing.tango_class: mod.Processing for mod in _pipeline_modules
}


def get_class(tango_class_name: str) -> Type:
    """Find a pipeline class by tango class name ("LimaProcessingXyz")

    Raise with some additional info if the class doesn't exist.
    """
    try:
        return by_name[tango_class_name]
    except KeyError as e:
        raise KeyError(
            f"Could not find processing class for {e} in '{__package__}'"
        ) from e
