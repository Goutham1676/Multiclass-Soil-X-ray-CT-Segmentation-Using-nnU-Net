"""Input/output utilities for 3D soil X-ray CT images."""

from pathlib import Path

import tifffile


def find_tiff_files(input_dir):
    """
    Find TIFF image stacks in an input directory.

    Parameters
    ----------
    input_dir : str or pathlib.Path
        Directory containing soil X-ray CT TIFF stacks.

    Returns
    -------
    list of pathlib.Path
        Sorted list of TIFF files.

    Raises
    ------
    FileNotFoundError
        If the directory does not exist or contains no TIFF files.
    """
    input_dir = Path(input_dir)

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Input directory not found: {input_dir}"
        )

    tif_files = sorted(
        list(input_dir.glob("*.tif"))
        + list(input_dir.glob("*.tiff"))
    )

    if not tif_files:
        raise FileNotFoundError(
            f"No TIFF files found in {input_dir}"
        )

    return tif_files


def select_tiff_file(input_dir):
    """
    Select a TIFF stack for processing.

    If only one TIFF file is present, it is selected automatically.
    If multiple TIFF files are present, the user is asked which file
    should be processed.

    Parameters
    ----------
    input_dir : str or pathlib.Path
        Directory containing soil X-ray CT TIFF stacks.

    Returns
    -------
    pathlib.Path
        Path to the selected TIFF file.
    """
    tif_files = find_tiff_files(input_dir)

    print(f"\nFound {len(tif_files)} TIFF file(s):")

    for number, file in enumerate(tif_files, start=1):
        print(f"  {number}. {file.name}")

    if len(tif_files) == 1:
        selected_file = tif_files[0]

    else:
        while True:
            try:
                selection = int(
                    input("\nSelect a TIFF file number: ")
                )

                if 1 <= selection <= len(tif_files):
                    selected_file = tif_files[selection - 1]
                    break

                print("Please select a valid file number.")

            except ValueError:
                print("Please enter a numeric file number.")

    print(f"\nSelected file: {selected_file.name}")

    return selected_file


def load_tiff(file_path):
    """
    Load a 3D TIFF stack and report basic image information.

    Parameters
    ----------
    file_path : str or pathlib.Path
        Path to the input TIFF stack.

    Returns
    -------
    numpy.ndarray
        Three-dimensional CT image ordered as Z, Y, X.

    Raises
    ------
    FileNotFoundError
        If the TIFF file cannot be found.
    ValueError
        If the input TIFF is not a 3D image stack.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"TIFF file not found: {file_path}"
        )

    image = tifffile.imread(file_path)

    if image.ndim != 3:
        raise ValueError(
            f"Expected a 3D TIFF stack, "
            f"but received shape {image.shape}"
        )

    print("\n--- Soil CT Image Information ---")
    print(f"File: {file_path.name}")
    print(f"Shape (Z, Y, X): {image.shape}")
    print(f"Number of slices: {image.shape[0]}")
    print(f"Height: {image.shape[1]}")
    print(f"Width: {image.shape[2]}")
    print(f"Data type: {image.dtype}")
    print(f"Minimum intensity: {image.min()}")
    print(f"Maximum intensity: {image.max()}")
    print(f"Mean intensity: {image.mean():.2f}")
    print(f"Standard deviation: {image.std():.2f}")

    return image