"""Preprocessing utilities for 3D soil X-ray CT images."""

import numpy as np


def normalization_decision(image, mode="ask"):
    """
    Apply or bypass image normalization.

    By default, the user is asked whether normalization should be
    performed. This keeps the preprocessing decision under user control.

    Parameters
    ----------
    image : numpy.ndarray
        Three-dimensional CT image.
    mode : {"ask", "as-is", "normalize"}, optional
        Normalization behavior.

        "ask"
            Ask the user whether to normalize.
        "as-is"
            Use the image without normalization.
        "normalize"
            Normalize nonzero voxels to 0-255.

        Default is "ask".

    Returns
    -------
    numpy.ndarray
        Prepared CT image.

    Raises
    ------
    ValueError
        If the supplied mode is invalid, the image contains no nonzero
        voxels, or the nonzero intensities are constant.
    """
    valid_modes = {
        "ask",
        "as-is",
        "normalize",
    }

    if mode not in valid_modes:
        raise ValueError(
            "mode must be 'ask', 'as-is', or 'normalize'."
        )

    if mode == "ask":
        print("\n--- Normalization ---")
        print("1. Use image as-is")
        print("2. Normalize image to 0-255")

        while True:
            choice = input(
                "Select option [1/2]: "
            ).strip()

            if choice == "1":
                mode = "as-is"
                break

            if choice == "2":
                mode = "normalize"
                break

            print("Please enter 1 or 2.")

    if mode == "as-is":
        print("Normalization bypassed.")
        return image

    nonzero_mask = image > 0

    if not np.any(nonzero_mask):
        raise ValueError(
            "Image contains no nonzero voxels."
        )

    values = image[
        nonzero_mask
    ].astype(np.float32)

    minimum = values.min()
    maximum = values.max()

    if maximum == minimum:
        raise ValueError(
            "Cannot normalize an image with constant intensity."
        )

    normalized = np.zeros(
        image.shape,
        dtype=np.uint8,
    )

    normalized_values = (
        (values - minimum)
        / (maximum - minimum)
        * 255
    )

    normalized[
        nonzero_mask
    ] = normalized_values.astype(np.uint8)

    print("Image normalized to 0-255.")

    return normalized