"""Napari utilities for interactive soil CT annotation."""

import numpy as np
import napari

from soilct_segmentation.annotation import (
    save_annotations,
)


def build_napari_colors(colors_by_id):
    """
    Convert dataset RGB colors to Napari-compatible RGBA colors.

    Parameters
    ----------
    colors_by_id : dict
        Mapping from label IDs to RGB values in the range 0-255.

    Returns
    -------
    dict
        Napari-compatible RGBA color dictionary.
    """
    colors = {
        int(label_id): [
            rgb[0] / 255,
            rgb[1] / 255,
            rgb[2] / 255,
            1.0,
        ]
        for label_id, rgb
        in colors_by_id.items()
    }

    # Any undefined labels are displayed transparently.
    colors[None] = [
        0,
        0,
        0,
        0,
    ]

    return colors


def open_annotation_viewer(
    image,
    labels,
    colors_by_id,
    opacity=0.65,
    blending="additive",
):
    """
    Open a CT volume and editable annotation layer in Napari.

    Parameters
    ----------
    image : numpy.ndarray
        Three-dimensional grayscale CT image.
    labels : numpy.ndarray
        Three-dimensional annotation volume.
    colors_by_id : dict
        Label colors from dataset_info.json.
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
    """
    viewer = napari.Viewer()

    viewer.add_image(
        image,
        name="Soil CT",
        colormap="gray",
    )

    napari_colors = build_napari_colors(
        colors_by_id
    )

    label_layer = viewer.add_labels(
        labels,
        name="Annotations",
        colormap=napari_colors,
        opacity=opacity,
        blending=blending,
    )

    return viewer, label_layer


def setup_annotation_saving(
    viewer,
    label_layer,
    annotation_file,
):
    """
    Enable manual and automatic annotation saving.

    Press Ctrl+S in Napari to save manually. The annotation is also
    saved automatically when the Napari window is closed.

    Parameters
    ----------
    viewer : napari.Viewer
        Active Napari viewer.
    label_layer : napari.layers.Labels
        Editable annotation layer.
    annotation_file : str or pathlib.Path
        Destination annotation TIFF.

    Returns
    -------
    callable
        Function that can be called to save the current annotations.
    """

    def save_current_annotations():
        """
        Save the currently edited Napari label volume.
        """
        saved_file = save_annotations(
            np.asarray(
                label_layer.data
            ),
            annotation_file,
        )

        print("\nAnnotations saved:")
        print(f"  {saved_file}")

        return saved_file

    @viewer.bind_key(
        "Control-S",
        overwrite=True,
    )
    def manual_save(viewer):
        save_current_annotations()

    qt_window = viewer.window._qt_window

    if not hasattr(
        qt_window,
        "_annotation_autosave_installed",
    ):
        original_close_event = (
            qt_window.closeEvent
        )

        def close_event_with_save(event):
            save_current_annotations()
            original_close_event(event)

        qt_window.closeEvent = (
            close_event_with_save
        )

        qt_window._annotation_autosave_installed = (
            True
        )

    return save_current_annotations