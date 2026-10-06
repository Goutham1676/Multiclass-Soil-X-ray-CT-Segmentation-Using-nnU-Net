import numpy as np


def normalize_image(image):
    """
    Normalize nonzero CT intensities to 0-255 while keeping background at 0.

    I_norm = (I - I_min) / (I_max - I_min) * 255
    """

    mask = image > 0

    if not np.any(mask):
        raise ValueError("Image contains no nonzero voxels.")

    values = image[mask].astype(np.float32)
    minimum = values.min()
    maximum = values.max()

    if minimum == maximum:
        raise ValueError("Cannot normalize an image with constant intensity.")

    normalized = np.zeros(image.shape, dtype=np.uint8)
    normalized[mask] = ((values - minimum) / (maximum - minimum) * 255).astype(np.uint8)

    print("Image stack normalized to 0-255.")
    return normalized