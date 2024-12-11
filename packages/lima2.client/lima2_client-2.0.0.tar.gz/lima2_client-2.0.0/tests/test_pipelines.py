"""Test suite for the Pipeline classes (lima2/client/pipelines/)"""

import pytest
import lima2.client.pipelines as pipelines


def test_get_by_name_nominal():
    for name in ["Legacy", "Smx", "Xpcs"]:
        pipeline_class = pipelines.get_class(f"LimaProcessing{name}")
        assert pipeline_class.tango_class == f"LimaProcessing{name}"


def test_get_by_name_invalid():
    with pytest.raises(KeyError):
        _ = pipelines.get_class("LimaProcessingInvalid")
