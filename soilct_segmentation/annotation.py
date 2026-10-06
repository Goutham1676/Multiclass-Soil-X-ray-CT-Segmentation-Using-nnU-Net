"""Utilities for preparing, loading, and saving soil CT annotations."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tifffile
from skimage.filters import threshold_otsu


def load_dataset_info(dataset_info_path):
    """
    Load annotation labels and colors from dataset_info.json.

    Parameters
    ----------
    dataset_info_path : str or pathlib.Path
        Path to the dataset configuration file.

    Returns
    -------
    labels_by_id : dict
        Mapping from label IDs to class names.
    labels_by_name : dict
        Mapping from class names to integer IDs.
    colors_by_id : dict
        Mapping from label IDs to RGB colors.
    """

    dataset_info_path = Path(dataset_info_path)

    if not dataset_info_path.exists():
        raise FileNotFoundError(f"Dataset information file not found: {dataset_info_path}")

    with open(dataset_info_path, encoding="utf-8") as file:
        dataset_info = json.load(file)

    labels_by_id = dataset_info["labels"]
    colors_by_id = dataset_info["colors"]
    labels_by_name = {name: int(label_id) for label_id, name in labels_by_id.items()}

    return labels_by_id, labels_by_name, colors_by_id


def calculate_otsu_threshold(image_slice):
    """
    Calculate the Otsu threshold using non-background pixels.

    Zero-valued pixels are excluded because they represent background
    outside the soil sample.
    """

    soil_pixels = image_slice[image_slice > 0]

    if soil_pixels.size == 0:
        raise ValueError("The selected slice contains no nonzero voxels.")

    return threshold_otsu(soil_pixels)


def create_matrix_mask(image_slice, lower_threshold, upper_threshold):
    """
    Create the initial soil matrix mask.

    Pixels between the lower and upper thresholds are assigned to the
    initial matrix mask.
    """

    if lower_threshold >= upper_threshold:
        raise ValueError("Lower threshold must be less than upper threshold.")

    return (image_slice > lower_threshold) & (image_slice < upper_threshold)


def select_matrix_thresholds(image_slice, slice_index=None, initial_upper_threshold=200):
    """
    Select the lower and upper thresholds for the initial matrix mask.

    Otsu thresholding is used as the starting lower threshold. The upper
    threshold is used to exclude brighter materials such as stones or
    mineral grains. The image and mask are displayed so the thresholds
    can be visually checked and adjusted.

    Parameters
    ----------
    image_slice : numpy.ndarray
        CT slice used for matrix initialization.
    slice_index : int, optional
        Slice number displayed in the figure title.
    initial_upper_threshold : float
        Starting upper threshold. Default is 200.

    Returns
    -------
    matrix_mask : numpy.ndarray
        Final matrix mask.
    lower_threshold : float
        Selected lower threshold.
    upper_threshold : float
        Selected upper threshold.
    """

    lower_threshold = float(calculate_otsu_threshold(image_slice))
    upper_threshold = float(initial_upper_threshold)
    
    if upper_threshold <= lower_threshold: 
        upper_threshold = float(image_slice.max())
    
    while True:
        matrix_mask = create_matrix_mask(image_slice, lower_threshold, upper_threshold)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        axes[0].imshow(image_slice, cmap="gray")
        axes[0].set_title(f"CT Slice {slice_index}" if slice_index is not None else "CT Slice")
        axes[0].axis("off")

        axes[1].imshow(matrix_mask, cmap="gray")
        axes[1].set_title(f"Matrix Mask: {lower_threshold:g} to {upper_threshold:g}")
        axes[1].axis("off")

        plt.tight_layout()
        plt.show()

        choice = input(
            f"Accept thresholds? Lower={lower_threshold:g}, "
            f"Upper={upper_threshold:g} (y/n): "
        ).lower()

        if choice == "y":
            break

        lower_threshold = float(input("Lower threshold: "))
        upper_threshold = float(input("Upper threshold: "))

    print(f"Selected thresholds: {lower_threshold:g} to {upper_threshold:g}")
    return matrix_mask, lower_threshold, upper_threshold


def get_annotation_file(input_file, annotation_dir):
    """
    Create the annotation filename for an input CT stack.

    The annotation uses the original TIFF name followed by _labels.tif.
    """

    input_file = Path(input_file)
    annotation_dir = Path(annotation_dir)

    return annotation_dir / f"{input_file.stem}_labels.tif"


def load_or_initialize_annotations(image, input_file, middle_slice,
                                   labels_by_name, annotation_dir, matrix_mask=None):
    """
    Load an existing annotation or create a new annotation volume.

    If an annotation already exists, it is loaded from disk. Otherwise,
    a new volume is initialized as ToPredict and the matrix mask is added
    to the selected middle slice.

    Parameters
    ----------
    image : numpy.ndarray
        Prepared 3D CT image.
    input_file : str or pathlib.Path
        Source CT TIFF file.
    middle_slice : int
        Slice used for the initial matrix annotation.
    labels_by_name : dict
        Mapping from class names to label IDs.
    annotation_dir : str or pathlib.Path
        Folder used to store annotation files.
    matrix_mask : numpy.ndarray, optional
        Initial matrix mask for a new annotation.

    Returns
    -------
    labels_3d : numpy.ndarray
        Annotation volume.
    annotation_file : pathlib.Path
        Path to the annotation TIFF.
    loaded_existing : bool
        True if an existing annotation was loaded.
    """

    annotation_dir = Path(annotation_dir)
    annotation_dir.mkdir(parents=True, exist_ok=True)

    annotation_file = get_annotation_file(input_file, annotation_dir)

    if annotation_file.exists():
        labels_3d = tifffile.imread(annotation_file)

        if labels_3d.shape != image.shape:
            raise ValueError(
                f"Saved annotation shape {labels_3d.shape} does not match image shape {image.shape}."
            )

        return labels_3d, annotation_file, True

    if matrix_mask is None:
        raise ValueError("matrix_mask is required when creating a new annotation.")

    labels_3d = np.full(image.shape, labels_by_name["ToPredict"], dtype=np.uint8)
    labels_3d[middle_slice][matrix_mask] = labels_by_name["Matrix"]

    return labels_3d, annotation_file, False


def save_annotations(annotation_data, annotation_file):
    """
    Save the annotation volume as an unsigned 8-bit TIFF stack.

    Parameters
    ----------
    annotation_data : numpy.ndarray
        3D annotation volume.
    annotation_file : str or pathlib.Path
        Output TIFF path.

    Returns
    -------
    pathlib.Path
        Path to the saved annotation.
    """

    annotation_file = Path(annotation_file)
    annotation_file.parent.mkdir(parents=True, exist_ok=True)

    annotation_data = np.asarray(annotation_data, dtype=np.uint8)
    tifffile.imwrite(annotation_file, annotation_data)

    return annotation_file