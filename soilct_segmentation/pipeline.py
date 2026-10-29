"""Main workflow for soil X-ray CT annotation."""

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from soilct_segmentation.annotation import (
    get_annotation_file,
    load_dataset_info,
    load_or_initialize_annotations,
    select_matrix_thresholds,
)
from soilct_segmentation.image_io import load_tiff, select_tiff_file
from soilct_segmentation.napari_tools import (
    open_annotation_viewer,
    setup_annotation_saving,
)
from soilct_segmentation.preprocessing import normalize_image


@dataclass
class AnnotationSession:
    """
    Store the image and annotation details for one session.

    Parameters
    ----------
    input_file : pathlib.Path
        Selected CT TIFF file.
    image : numpy.ndarray
        Original CT stack.
    prepared_image : numpy.ndarray
        CT stack after preprocessing.
    middle_slice : int
        Index of the middle slice.
    labels_3d : numpy.ndarray or None
        Annotation volume, if initialized or loaded.
    annotation_file : pathlib.Path
        Path to the annotation TIFF.
    labels_by_id : dict
        Label IDs and their class names.
    labels_by_name : dict
        Class names and their label IDs.
    colors_by_id : dict
        Colors assigned to the annotation classes.
    loaded_existing : bool
        Whether an existing annotation was loaded.
    lower_threshold : float or None
        Selected lower matrix threshold.
    upper_threshold : float or None
        Selected upper matrix threshold.
    selection : dict or None
        Threshold slider results for a new annotation.
    """

    input_file: Path
    image: np.ndarray
    prepared_image: np.ndarray
    middle_slice: int
    labels_3d: np.ndarray | None
    annotation_file: Path
    labels_by_id: dict
    labels_by_name: dict
    colors_by_id: dict
    loaded_existing: bool
    lower_threshold: float | None = None
    upper_threshold: float | None = None
    selection: dict | None = None

    def summary(self):
        """Print the current annotation details."""

        print("\nAnnotation Session")
        print(f"Input: {self.input_file.name}")
        print(f"Image shape: {self.prepared_image.shape}")
        print(f"Middle slice: {self.middle_slice}")
        print(f"Annotation file: {self.annotation_file}")

        if self.loaded_existing:
            print("Status: Existing annotation loaded")
        else:
            print("Status: New annotation initialized")
            print(
                f"Matrix thresholds: {self.lower_threshold:g} "
                f"to {self.upper_threshold:g}"
            )


def show_image_inspection(image, middle_slice):
    """
    Display the middle CT slice and intensity histogram.

    The histogram uses nonzero voxels from the full CT stack.

    Parameters
    ----------
    image : numpy.ndarray
        Input CT stack.
    middle_slice : int
        Index of the slice to display.
    """

    middle_image = image[middle_slice]

    plt.figure(figsize=(8, 8))
    plt.imshow(middle_image, cmap="gray")
    plt.title(f"Middle CT Slice (Index {middle_slice})")
    plt.axis("off")
    plt.show()

    nonzero = image[image > 0]

    if nonzero.size == 0:
        print("No nonzero voxels available for histogram.")
        return

    plt.figure(figsize=(8, 5))
    plt.hist(nonzero.ravel(), bins=256)
    plt.xlabel("Voxel Intensity")
    plt.ylabel("Frequency")
    plt.title("Intensity Distribution of Soil CT Stack")
    plt.show()


def prepare_annotation_session(
    input_dir="soilct_segmentation/Input data",
    dataset_info_path="dataset_info.json",
    annotation_dir="soilct_segmentation/Annotations",
    initial_upper_threshold=200,
    show_inspection=True,
):
    """
    Load and prepare a CT stack for annotation.

    Checks for an existing annotation. If none is found, the middle
    slice is used to select the initial matrix thresholds.

    Parameters
    ----------
    input_dir : str or pathlib.Path
        Folder containing the CT TIFF stack.
    dataset_info_path : str or pathlib.Path
        Path to dataset_info.json.
    annotation_dir : str or pathlib.Path
        Folder used to save annotation TIFF files.
    initial_upper_threshold : float
        Starting upper threshold for matrix selection.
    show_inspection : bool
        Whether to display the middle slice and histogram.

    Returns
    -------
    AnnotationSession
        Session containing the image and annotation information.
    """

    input_file = select_tiff_file(input_dir)
    image = load_tiff(input_file)

    middle_slice = (image.shape[0] - 1) // 2
    print(f"\nSelected middle slice: {middle_slice}")

    if show_inspection:
        show_image_inspection(image, middle_slice)

    prepared_image = normalize_image(image)

    labels_by_id, labels_by_name, colors_by_id = load_dataset_info(dataset_info_path)
    annotation_file = get_annotation_file(input_file, annotation_dir)

    lower_threshold = None
    upper_threshold = None
    selection = None

    if annotation_file.exists():
        print("\nExisting annotation found.")

        labels_3d, annotation_file, loaded_existing = load_or_initialize_annotations(
            prepared_image,
            input_file,
            middle_slice,
            labels_by_name,
            annotation_dir,
        )

    else:
        print("\nNo existing annotation found.")

        middle_image = prepared_image[middle_slice]

        selection = select_matrix_thresholds(
            middle_image,
            slice_index=middle_slice,
            initial_upper_threshold=initial_upper_threshold,
        )

        labels_3d = None
        loaded_existing = False

    session = AnnotationSession(
        input_file=Path(input_file),
        image=image,
        prepared_image=prepared_image,
        middle_slice=middle_slice,
        labels_3d=labels_3d,
        annotation_file=Path(annotation_file),
        labels_by_id=labels_by_id,
        labels_by_name=labels_by_name,
        colors_by_id=colors_by_id,
        loaded_existing=loaded_existing,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        selection=selection,
    )

    if session.loaded_existing:
        session.summary()

    return session


def launch_annotation_session(session, opacity=0.65, blending="additive"):
    """
    Open the CT stack and annotation labels in Napari.

    For a new annotation, initialize the matrix mask using the accepted
    thresholds. Save annotations manually with Ctrl+S or when Napari closes.

    Parameters
    ----------
    session : AnnotationSession
        Session returned by prepare_annotation_session().
    opacity : float
        Opacity of the annotation layer.
    blending : str
        Napari blending mode.

    Returns
    -------
    viewer
        Napari viewer.
    label_layer
        Editable annotation layer.
    save_current_annotations
        Function used to save the annotation.
    """

    if session.selection is not None:
        if not session.selection["accepted"]:
            raise RuntimeError("Click Accept on the threshold slider first.")

        session.lower_threshold = session.selection["lower"]
        session.upper_threshold = session.selection["upper"]

        (
            session.labels_3d,
            session.annotation_file,
            session.loaded_existing,
        ) = load_or_initialize_annotations(
            session.prepared_image,
            session.input_file,
            session.middle_slice,
            session.labels_by_name,
            session.annotation_file.parent,
            session.selection["mask"],
        )

        session.selection = None
        session.summary()

    viewer, label_layer = open_annotation_viewer(
        session.prepared_image,
        session.labels_3d,
        session.colors_by_id,
        opacity=opacity,
        blending=blending,
    )

    save_current_annotations = setup_annotation_saving(
        viewer, label_layer, session.annotation_file
    )

    return viewer, label_layer, save_current_annotations
