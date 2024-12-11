"""Test suite for utility functions (lima2/client/utils.py)"""

from lima2.client.utils import docstring_from


def test_docstring_from():
    def parent():
        """cafedeca"""
        pass

    @docstring_from(parent)
    def child():
        """deadbeef"""
        pass

    assert child.__doc__ == "cafedeca"
