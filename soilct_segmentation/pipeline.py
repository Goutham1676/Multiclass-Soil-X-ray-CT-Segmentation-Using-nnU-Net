"""
High-level workflow for multiclass soil X-ray CT annotation.

This module combines image loading, inspection, preprocessing,
threshold initialization, annotation persistence, and Napari
visualization into a simple user-facing workflow.
"""

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from soilct_segmentation.annotation import (
    get_annotation_file,
    load_dataset_info,
    load_or_initialize_annotations,
    select_matrix_thresholds,
    summarize_annotations,
)
from soilct_segmentation.image_io import (
    load_tiff,
    select_tiff_file,
)
from soilct_segmentation.napari_tools import (
    open_annotation_viewer,
    setup_annotation_saving,
)
from soilct_segmentation.preprocessing import (
    normalization_decision,
)


@dataclass
class AnnotationSession:
    """
    Store information associated with one annotation session.

    Parameters
    ----------
    input_file : pathlib.Path
        Selected source CT TIFF.
    image : numpy.ndarray
        Original CT volume.
    prepared_image : numpy.ndarray
        CT volume after preprocessing.
    middle_slice : int
        Representative middle-slice index.
    labels_3d : numpy.ndarray
        Current 3D annotation volume.
    annotation_file : pathlib.Path
        Annotation TIFF path.
    labels_by_id : dict
        Mapping from label IDs to class names.
    labels_by_name : dict
        Mapping from class names to integer IDs.
    colors_by_id : dict
        Annotation colors.
    loaded_existing : bool
        Whether an existing annotation was loaded.
    lower_threshold : float or None
        Accepted lower matrix threshold.
    upper_threshold : float or None
        Accepted upper matrix threshold.
    """

    input_file: Path
    image: np.ndarray
    prepared_image: np.ndarray
    middle_slice: int
    labels_3d: np.ndarray
    annotation_file: Path
    labels_by_id: dict
    labels_by_name: dict
    colors_by_id: dict
    loaded_existing: bool
    lower_threshold: float | None = None
    upper_threshold: float | None = None

    def summary(self):
        """
        Print a concise summary of the annotation session.
        """
        print("\n=== Annotation Session ===")
        print(f"Input: {self.input_file.name}")
        print(
            f"Image shape: "
            f"{self.prepared_image.shape}"
        )
        print(
            f"Middle slice: "
            f"{self.middle_slice}"
        )
        print(
            f"Annotation file: "
            f"{self.annotation_file}"
        )

        if self.loaded_existing:
            print(
                "Status: Existing annotation loaded"
            )

        else:
            print(
                "Status: New annotation initialized"
            )

            print(
                f"Matrix thresholds: "
                f"{self.lower_threshold:g} - "
                f"{self.upper_threshold:g}"
            )


def show_image_inspection(
    image,
    middle_slice,
):
    """
    Display a representative CT slice and intensity histogram.

    Zero-valued background voxels are excluded from the histogram.

    Parameters
    ----------
    image : numpy.ndarray
        Three-dimensional CT image.
    middle_slice : int
        Slice index to display.
    """
    middle_image = image[
        middle_slice
    ]

    plt.figure(figsize=(8, 8))

    plt.imshow(
        middle_image,
        cmap="gray",
    )

    plt.title(
        f"Middle CT Slice "
        f"(Index {middle_slice})"
    )

    plt.axis("off")
    plt.show()

    nonzero = image[
        image > 0
    ]

    if nonzero.size == 0:
        print(
            "No nonzero voxels available "
            "for histogram."
        )
        return

    plt.figure(figsize=(8, 5))

    plt.hist(
        nonzero.ravel(),
        bins=256,
    )

    plt.xlabel(
        "Voxel Intensity"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.title(
        "Intensity Distribution "
        "of Soil CT Stack"
    )

    plt.show()


def prepare_annotation_session(
    input_dir="soilct_segmentation/Input data",
    dataset_info_path="dataset_info.json",
    annotation_dir="soilct_segmentation/Annotations",
    normalization_mode="ask",
    initial_upper_threshold=190,
    show_inspection=True,
):
    """
    Prepare a soil CT image for interactive multiclass annotation.

    This function performs the complete pre-Napari workflow:

    1. Finds and selects an input TIFF.
    2. Loads the 3D CT image.
    3. Selects a representative middle slice.
    4. Displays the CT slice and intensity histogram.
    5. Asks whether normalization should be applied.
    6. Loads annotation-class information.
    7. Checks for an existing saved annotation.
    8. If no annotation exists, performs interactive threshold selection.
    9. Creates or loads the 3D annotation volume.

    Parameters
    ----------
    input_dir : str or pathlib.Path, optional
        Directory containing input CT TIFF files.
    dataset_info_path : str or pathlib.Path, optional
        Path to dataset_info.json.
    annotation_dir : str or pathlib.Path, optional
        Directory used to save annotation TIFF files.
    normalization_mode : {"ask", "as-is", "normalize"}, optional
        Normalization behavior. Default is "ask", so the user makes
        the preprocessing decision.
    initial_upper_threshold : float, optional
        Proposed starting upper matrix threshold. Default is 190.
        The user can modify this interactively.
    show_inspection : bool, optional
        Whether to display the middle slice and histogram.
        Default is True.

    Returns
    -------
    AnnotationSession
        Prepared annotation session.
    """
    input_file = select_tiff_file(
        input_dir
    )

    image = load_tiff(
        input_file
    )

    middle_slice = (
        image.shape[0] - 1
    ) // 2

    print(
        f"\nSelected middle slice: "
        f"{middle_slice}"
    )

    if show_inspection:
        show_image_inspection(
            image,
            middle_slice,
        )

    # The user is asked about normalization by default.
    prepared_image = normalization_decision(
        image,
        mode=normalization_mode,
    )

    (
        labels_by_id,
        labels_by_name,
        colors_by_id,
    ) = load_dataset_info(
        dataset_info_path
    )

    annotation_file = get_annotation_file(
        input_file,
        annotation_dir,
    )

    lower_threshold = None
    upper_threshold = None

    if annotation_file.exists():

        print("\nExisting annotation found.")
        print(
            "The saved annotation will be loaded."
        )
        print(
            "Matrix threshold initialization "
            "is therefore not required."
        )

        (
            labels_3d,
            annotation_file,
            loaded_existing,
        ) = load_or_initialize_annotations(
            image=prepared_image,
            input_file=input_file,
            middle_slice=middle_slice,
            labels_by_name=labels_by_name,
            annotation_dir=annotation_dir,
            matrix_mask=None,
        )

    else:

        print("\nNo existing annotation found.")
        print(
            "Starting interactive matrix initialization."
        )

        middle_image = prepared_image[
            middle_slice
        ]

        (
            matrix_mask,
            lower_threshold,
            upper_threshold,
        ) = select_matrix_thresholds(
            middle_image,
            slice_index=middle_slice,
            initial_upper_threshold=(
                initial_upper_threshold
            ),
        )

        (
            labels_3d,
            annotation_file,
            loaded_existing,
        ) = load_or_initialize_annotations(
            image=prepared_image,
            input_file=input_file,
            middle_slice=middle_slice,
            labels_by_name=labels_by_name,
            annotation_dir=annotation_dir,
            matrix_mask=matrix_mask,
        )

    session = AnnotationSession(
        input_file=Path(input_file),
        image=image,
        prepared_image=prepared_image,
        middle_slice=middle_slice,
        labels_3d=labels_3d,
        annotation_file=Path(
            annotation_file
        ),
        labels_by_id=labels_by_id,
        labels_by_name=labels_by_name,
        colors_by_id=colors_by_id,
        loaded_existing=loaded_existing,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
    )

    session.summary()

    summarize_annotations(
        session.labels_3d,
        session.labels_by_id,
    )

    return session


def launch_annotation_session(
    session,
    opacity=0.65,
    blending="additive",
):
    """
    Open a prepared annotation session in Napari.

    The CT volume and current annotation are displayed together.
    Ctrl+S saves the annotation manually, and closing Napari saves
    the annotation automatically.

    Parameters
    ----------
    session : AnnotationSession
        Session created by prepare_annotation_session().
    opacity : float, optional
        Annotation-layer opacity. Default is 0.65.
    blending : str, optional
        Napari blending mode. Default is "additive".

    Returns
    -------
    viewer : napari.Viewer
        Napari viewer.
    label_layer : napari.layers.Labels
        Editable annotation layer.
    save_current_annotations : callable
        Function that manually saves the current annotation.
    """
    viewer, label_layer = (
        open_annotation_viewer(
            image=session.prepared_image,
            labels=session.labels_3d,
            colors_by_id=session.colors_by_id,
            opacity=opacity,
            blending=blending,
        )
    )

    save_current_annotations = (
        setup_annotation_saving(
            viewer,
            label_layer,
            session.annotation_file,
        )
    )

    print("\nNapari annotation session ready.")
    print(
        "  Ctrl+S       -> save annotations"
    )
    print(
        "  Close Napari -> save automatically"
    )
    print(
        f"  Output       -> "
        f"{session.annotation_file}"
    )

    return (
        viewer,
        label_layer,
        save_current_annotations,
    )