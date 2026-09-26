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
        Mapping from class names to integer label IDs.
    colors_by_id : dict
        Mapping from label IDs to RGB color values.

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist.
    """
    dataset_info_path = Path(dataset_info_path)

    if not dataset_info_path.exists():
        raise FileNotFoundError(
            f"Dataset information file not found: "
            f"{dataset_info_path}"
        )

    with open(
        dataset_info_path,
        "r",
        encoding="utf-8",
    ) as file:
        dataset_info = json.load(file)

    labels_by_id = dataset_info["labels"]
    colors_by_id = dataset_info["colors"]

    labels_by_name = {
        name: int(label_id)
        for label_id, name
        in labels_by_id.items()
    }

    return (
        labels_by_id,
        labels_by_name,
        colors_by_id,
    )


def calculate_otsu_threshold(image_slice):
    """
    Calculate an Otsu threshold using non-background pixels.

    Zero-valued pixels are excluded because they represent the
    background outside the soil sample.

    Parameters
    ----------
    image_slice : numpy.ndarray
        Two-dimensional CT slice.

    Returns
    -------
    float
        Calculated Otsu threshold.

    Raises
    ------
    ValueError
        If the selected slice contains no nonzero pixels.
    """
    soil_pixels = image_slice[
        image_slice > 0
    ]

    if soil_pixels.size == 0:
        raise ValueError(
            "The selected slice contains no nonzero voxels."
        )

    return threshold_otsu(soil_pixels)


def create_matrix_mask(
    image_slice,
    lower_threshold,
    upper_threshold,
):
    """
    Create an initial matrix mask from a CT slice.

    Pixels with intensities between the lower and upper thresholds
    are classified as initial soil matrix.

    Parameters
    ----------
    image_slice : numpy.ndarray
        Two-dimensional CT slice.
    lower_threshold : float
        Lower matrix threshold.
    upper_threshold : float
        Upper matrix threshold.

    Returns
    -------
    numpy.ndarray
        Boolean matrix mask.

    Raises
    ------
    ValueError
        If lower_threshold is not smaller than upper_threshold.
    """
    if lower_threshold >= upper_threshold:
        raise ValueError(
            "lower_threshold must be smaller "
            "than upper_threshold."
        )

    return (
        (image_slice > lower_threshold)
        & (image_slice < upper_threshold)
    )


def select_matrix_thresholds(
    image_slice,
    slice_index=None,
    initial_upper_threshold=190,
):
    """
    Interactively select lower and upper matrix thresholds.

    Otsu thresholding supplies the initial lower threshold. An initial
    upper threshold is also proposed to exclude very bright materials
    such as stones or mineral grains.

    The original CT slice and resulting matrix mask are displayed
    side-by-side. The user can accept the thresholds or repeatedly
    adjust them.

    Parameters
    ----------
    image_slice : numpy.ndarray
        Two-dimensional CT slice.
    slice_index : int, optional
        Slice number used in the figure title.
    initial_upper_threshold : float, optional
        Starting upper matrix threshold. Default is 190.

    Returns
    -------
    matrix_mask : numpy.ndarray
        Accepted matrix mask.
    lower_threshold : float
        Accepted lower threshold.
    upper_threshold : float
        Accepted upper threshold.
    """
    lower_threshold = float(
        calculate_otsu_threshold(image_slice)
    )

    image_min = float(image_slice.min())
    image_max = float(image_slice.max())

    upper_threshold = min(
        float(initial_upper_threshold),
        image_max,
    )

    if upper_threshold <= lower_threshold:
        upper_threshold = image_max

    if upper_threshold <= lower_threshold:
        raise ValueError(
            "Unable to create a valid threshold range."
        )

    while True:
        matrix_mask = create_matrix_mask(
            image_slice,
            lower_threshold,
            upper_threshold,
        )

        fig, axes = plt.subplots(
            1,
            2,
            figsize=(12, 6),
        )

        axes[0].imshow(
            image_slice,
            cmap="gray",
        )

        if slice_index is None:
            axes[0].set_title(
                "Original CT Slice"
            )
        else:
            axes[0].set_title(
                f"Original CT Slice "
                f"(Index {slice_index})"
            )

        axes[0].axis("off")

        axes[1].imshow(
            matrix_mask,
            cmap="gray",
        )

        axes[1].set_title(
            "Matrix Initialization\n"
            f"{lower_threshold:g} < intensity < "
            f"{upper_threshold:g}"
        )

        axes[1].axis("off")

        plt.tight_layout()
        plt.show()

        choice = input(
            "Accept these thresholds? "
            "[Y = accept / N = adjust]: "
        ).strip().lower()

        if choice == "y":
            break

        if choice == "n":
            try:
                lower_input = input(
                    f"Enter lower threshold "
                    f"[{lower_threshold:g}]: "
                ).strip()

                upper_input = input(
                    f"Enter upper threshold "
                    f"[{upper_threshold:g}]: "
                ).strip()

                new_lower = (
                    lower_threshold
                    if lower_input == ""
                    else float(lower_input)
                )

                new_upper = (
                    upper_threshold
                    if upper_input == ""
                    else float(upper_input)
                )

                if new_lower >= new_upper:
                    print(
                        "Lower threshold must be less "
                        "than upper threshold."
                    )
                    continue

                if not (
                    image_min <= new_lower <= image_max
                    and
                    image_min <= new_upper <= image_max
                ):
                    print(
                        f"Thresholds must be between "
                        f"{image_min:g} and "
                        f"{image_max:g}."
                    )
                    continue

                lower_threshold = new_lower
                upper_threshold = new_upper

            except ValueError:
                print(
                    "Please enter numeric threshold values."
                )

        else:
            print("Please enter Y or N.")

    print("\nThresholds accepted.")
    print(f"Lower threshold: {lower_threshold:g}")
    print(f"Upper threshold: {upper_threshold:g}")

    soil_area = image_slice > 0

    if soil_area.sum() > 0:
        coverage = (
            100
            * matrix_mask.sum()
            / soil_area.sum()
        )

        print(
            f"Matrix coverage within soil region: "
            f"{coverage:.2f}%"
        )

    return (
        matrix_mask,
        lower_threshold,
        upper_threshold,
    )


def get_annotation_file(
    input_file,
    annotation_dir,
):
    """
    Construct the annotation filename for an input CT stack.

    Parameters
    ----------
    input_file : str or pathlib.Path
        Input TIFF path.
    annotation_dir : str or pathlib.Path
        Directory where annotation files are stored.

    Returns
    -------
    pathlib.Path
        Annotation TIFF path.
    """
    input_file = Path(input_file)
    annotation_dir = Path(annotation_dir)

    return (
        annotation_dir
        / f"{input_file.stem}_labels.tif"
    )


def load_or_initialize_annotations(
    image,
    input_file,
    middle_slice,
    labels_by_name,
    annotation_dir,
    matrix_mask=None,
):
    """
    Load an existing annotation or initialize a new one.

    If an annotation TIFF already exists, it is loaded automatically.
    Otherwise, a new 3D volume is created using ToPredict everywhere
    and Matrix on the selected slice where matrix_mask is True.

    Parameters
    ----------
    image : numpy.ndarray
        Three-dimensional CT image.
    input_file : str or pathlib.Path
        Path to the source CT TIFF.
    middle_slice : int
        Slice used for the initial dense annotation.
    labels_by_name : dict
        Mapping from class names to integer IDs.
    annotation_dir : str or pathlib.Path
        Annotation output directory.
    matrix_mask : numpy.ndarray, optional
        Initial matrix mask. Required only for a new annotation.

    Returns
    -------
    labels_3d : numpy.ndarray
        Three-dimensional annotation volume.
    annotation_file : pathlib.Path
        Annotation TIFF path.
    loaded_existing : bool
        True if an existing annotation was loaded.
    """
    annotation_dir = Path(annotation_dir)

    annotation_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    annotation_file = get_annotation_file(
        input_file,
        annotation_dir,
    )

    if annotation_file.exists():
        labels_3d = tifffile.imread(
            annotation_file
        )

        if labels_3d.shape != image.shape:
            raise ValueError(
                f"Saved annotation shape "
                f"{labels_3d.shape} does not match "
                f"image shape {image.shape}."
            )

        return (
            labels_3d,
            annotation_file,
            True,
        )

    if matrix_mask is None:
        raise ValueError(
            "matrix_mask is required when creating "
            "a new annotation volume."
        )

    labels_3d = np.full(
        image.shape,
        labels_by_name["ToPredict"],
        dtype=np.uint8,
    )

    labels_3d[
        middle_slice
    ][
        matrix_mask
    ] = labels_by_name["Matrix"]

    return (
        labels_3d,
        annotation_file,
        False,
    )


def summarize_annotations(
    labels_3d,
    labels_by_id,
):
    """
    Print the annotation classes currently present.

    Parameters
    ----------
    labels_3d : numpy.ndarray
        Three-dimensional annotation volume.
    labels_by_id : dict
        Mapping from label IDs to class names.
    """
    unique_labels, counts = np.unique(
        labels_3d,
        return_counts=True,
    )

    print("\nLabels currently present:")
    print("-------------------------")

    for label_id, count in zip(
        unique_labels,
        counts,
    ):
        class_name = labels_by_id.get(
            str(label_id),
            "Unknown",
        )

        print(
            f"  {label_id}: "
            f"{class_name} -> "
            f"{count:,} voxels"
        )


def save_annotations(
    annotation_data,
    annotation_file,
):
    """
    Save a 3D annotation volume as an unsigned 8-bit TIFF stack.

    Parameters
    ----------
    annotation_data : numpy.ndarray
        Three-dimensional annotation array.
    annotation_file : str or pathlib.Path
        Destination annotation TIFF.

    Returns
    -------
    pathlib.Path
        Saved annotation path.
    """
    annotation_file = Path(annotation_file)

    annotation_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    annotation_data = np.asarray(
        annotation_data,
        dtype=np.uint8,
    )

    tifffile.imwrite(
        annotation_file,
        annotation_data,
    )

    return annotation_file