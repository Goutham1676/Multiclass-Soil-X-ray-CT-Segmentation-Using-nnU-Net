"""Tests for core soil X-ray CT segmentation utilities."""

import numpy as np
import pytest

from soilct_segmentation.annotation import (
    calculate_otsu_threshold,
    create_matrix_mask,
)


def test_create_matrix_mask_known_values():
    """Matrix mask should include only values inside the threshold range."""

    image = np.array(
        [
            [0, 50, 100],
            [120, 150, 200],
            [210, 220, 230],
        ],
        dtype=np.uint8,
    )

    mask = create_matrix_mask(
        image,
        lower_threshold=100,
        upper_threshold=210,
    )

    expected = np.array(
        [
            [False, False, False],
            [True, True, True],
            [False, False, False],
        ]
    )

    assert np.array_equal(mask, expected)


def test_create_matrix_mask_invalid_thresholds():
    """Lower threshold must be smaller than the upper threshold."""

    image = np.array(
        [
            [100, 120],
            [140, 160],
        ],
        dtype=np.uint8,
    )

    with pytest.raises(ValueError):
        create_matrix_mask(
            image,
            lower_threshold=180,
            upper_threshold=120,
        )


def test_calculate_otsu_threshold_ignores_zero_background():
    """Otsu calculation should ignore zero-valued background pixels."""

    image = np.array(
        [
            [0, 0, 0, 0],
            [0, 50, 50, 200],
            [0, 50, 200, 200],
        ],
        dtype=np.uint8,
    )

    threshold = calculate_otsu_threshold(image)

    assert threshold > 0
    assert threshold < 200


def test_calculate_otsu_threshold_empty_soil_region():
    """An image containing only background should raise an error."""

    image = np.zeros(
        (5, 5),
        dtype=np.uint8,
    )

    with pytest.raises(ValueError):
        calculate_otsu_threshold(image)