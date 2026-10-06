"""Napari tools for interactive soil CT annotation."""

import napari
import numpy as np

from soilct_segmentation.annotation import save_annotations


def build_napari_colors(colors_by_id):
    """
    Convert RGB colors from dataset_info.json to Napari RGBA colors.

    RGB values are converted from 0-255 to 0-1. Undefined labels are
    displayed as transparent.
    """

    colors = {
        int(label_id): [rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, 1.0]
        for label_id, rgb in colors_by_id.items()
    }

    colors[None] = [0, 0, 0, 0]
    return colors


def open_annotation_viewer(image, labels, colors_by_id,
                           opacity=0.65, blending="additive"):
    """
    Open the CT image and annotation labels in Napari.

    Parameters
    ----------
    image : numpy.ndarray
        3D grayscale CT image.
    labels : numpy.ndarray
        3D annotation volume.
    colors_by_id : dict
        Label colors from dataset_info.json.
    opacity : float
        Annotation layer opacity.
    blending : str
        Napari blending mode.

    Returns
    -------
    viewer
        Napari viewer.
    label_layer
        Editable annotation layer.
    """

    viewer = napari.Viewer()
    viewer.add_image(image, name="Soil CT", colormap="gray")

    napari_colors = build_napari_colors(colors_by_id)

    label_layer = viewer.add_labels(
        labels,
        name="Annotations",
        colormap=napari_colors,
        opacity=opacity,
        blending=blending
    )

    return viewer, label_layer


def setup_annotation_saving(viewer, label_layer, annotation_file):
    """
    Set up manual and automatic saving for the annotation.

    Ctrl+S saves the current labels manually. Closing the Napari window
    also saves the annotation automatically.

    Parameters
    ----------
    viewer : napari.Viewer
        Active Napari viewer.
    label_layer : napari.layers.Labels
        Editable annotation layer.
    annotation_file : str or pathlib.Path
        Output annotation TIFF.

    Returns
    -------
    callable
        Function that saves the current annotation.
    """

    def save_current_annotations():
        """Save the current Napari annotation layer."""

        annotation_data = np.asarray(label_layer.data, dtype=np.uint8)
        saved_file = save_annotations(annotation_data, annotation_file)

        print(f"Annotations saved to: {saved_file}")
        return saved_file

    @viewer.bind_key("Control-S", overwrite=True)
    def manual_save(viewer):
        save_current_annotations()

    qt_window = viewer.window._qt_window

    if not hasattr(qt_window, "_annotation_autosave_installed"):
        original_close_event = qt_window.closeEvent

        def close_event_with_save(event):
            save_current_annotations()
            original_close_event(event)

        qt_window.closeEvent = close_event_with_save
        qt_window._annotation_autosave_installed = True

    return save_current_annotations