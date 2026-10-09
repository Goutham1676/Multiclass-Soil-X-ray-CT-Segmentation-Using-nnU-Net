"""Check that the required project libraries can be imported."""

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "numpy",
        "matplotlib",
        "skimage",
        "tifffile",
        "napari",
        "jupyterlab",
        "qtpy.QtWidgets",
    ],
)
def test_required_library_import(module_name):
    importlib.import_module(module_name)