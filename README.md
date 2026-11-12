# Multiclass Soil X-ray CT Segmentation Using nnU-Net

This project focuses on multiclass segmentation of soil X-ray CT images using
nnU-Net. The classes of interest are soil matrix, stones, organic matter,
roots, biopores, and other pores.

The goal is to build a workflow that starts with manual annotation of ground
truth labels and continues through nnU-Net training, prediction, and evaluation.

## Project Workflow

The current workflow focuses on preparing soil X-ray CT images and creating multiclass annotations.

1. Load, inspect, and normalize the CT stack.
2. Use Otsu thresholding and an interactive slider to select the initial soil matrix.
3. Open the image in Napari for manual annotation and refinement.
4. Save the annotations as a 3D TIFF stack for continued editing.

Existing annotations are loaded directly without repeating the threshold selection.

The next phase will involve preparing the annotated images for nnU-Net training, prediction, and evaluation using class-wise Dice scores.

## Repository Structure

- `paper/` – project proposal and later manuscript files
- `soilct_segmentation/` – Python code for the project
- `environment.yml` – software environment information
- `pyproject.toml` – Python project configuration
- `01_soilct_annotation.ipynb` – current preprocessing and Napari annotation workflow
- `Makefile` – commands for environment setup and automated testing



## Setup, Testing and Validation

### 1. Clone the repository

Clone the project from GitHub and navigate to the repository directory.

```bash
git clone https://github.com/Goutham1676/Multiclass-Soil-X-ray-CT-Segmentation-Using-nnU-Net.git
cd Multiclass-Soil-X-ray-CT-Segmentation-Using-nnU-Net
```

### 2. Create the Conda environment

Make sure Conda is installed. If not, download and install [Miniforge3](https://github.com/conda-forge/miniforge), which provides a lightweight Conda installation.
Create the environment using the provided `environment.yml` file.

```bash
conda env create -f environment.yml
conda activate soilct
```

The environment includes the Python dependencies required for preprocessing, annotation, and testing.

### 3. Check the environment

From the repository root, run:

```bash
make help
make test
```

`make help` displays the available automation commands, and `make test` runs the automated tests.

The expected result is 11 passing tests. Some warnings may appear from Napari-related dependencies, but the UI works fine.

### 4. Start JupyterLab

With the `soilct` environment activated, run:

```bash
jupyter lab
```

Open `01_soilct_annotation.ipynb`.

This notebook provides the workflow for preprocessing soil CT images, selecting initial thresholds, and manually refining annotations in Napari. A graphical desktop environment is required for Napari.

### 5. Run the annotation workflow

1. Place a 3D TIFF stack (`.tif` or `.tiff`) in `soilct_segmentation/Input data/`, or change `input_dir` to use a folder on your local disk.
2. Open `01_soilct_annotation.ipynb` and run the cells in order.
3. Inspect the image, adjust the threshold slider, and click **Accept**.
4. Open Napari to inspect the initial segmentation and make manual edits if needed.
5. Press `Ctrl+S` or close the Napari window to save.

Annotations are saved as 3D TIFF files in `soilct_segmentation/Annotations/` and can be reopened for further editing.


### Assumptions and Limitations

- Zero-valued voxels are treated as background during normalization and Otsu threshold calculation.

- Initial matrix labels are based on intensity thresholds and require manual review.

- Workflow validation currently covers the input CT stack. nnU-Net training, prediction, and segmentation accuracy have not yet been evaluated.


## Current Status

### Milestone 1

Milestone 1 established:

- the initial GitHub repository
- the project proposal
- the planned project workflow
- the initial software environment
- the initial repository structure

### Milestone 2

Milestone 2 established the initial working environment for soil X-ray CT segmentation and annotation. The main outcomes are:

- created the preprocessing environment for loading, inspecting, and normalizing a subset of 3D soil X-ray CT images
- developed an initial segmentation workflow using Otsu thresholding with user-adjustable thresholds
- integrated a Napari-based interface for multiclass annotation and manual refinement
- added support for saving and reloading annotation volumes for continued editing
- organized the workflow into reusable Python modules with a simplified notebook interface
- added basic automated tests and validated the workflow through GitHub Actions

### Milestone 3

For this milestone, I added tests to check that the required libraries can be imported. All 11 tests passed using both pytest and `make test`. 
I also checked that edits made in Napari were saved and still present after reopening the annotation. 
Instructions for running the tests and the current assumptions and limitations are included above.
These results will support the testing and software quality discussion in the final report.

### Milestone 4

For this milestone, I updated the README with setup instructions, annotation steps, and input and output details. I also reviewed the Python docstrings and notebook documentation.

All 11 tests passed using make check, and Ruff found no issues.

These updates will help others run the workflow and document the methods in the final JOSS-style paper.

### Milestone 5

For this milestone, I focused on making the annotation workflow easier for others to set up and reproduce. I updated the README with instructions for installing the environment, running the annotation notebook, and checking the project using the Makefile.

All 11 tests passed using `make test`, and Ruff reported no issues. The main workflow can be run through JupyterLab, with Napari used for viewing and editing annotations.


## Next Steps

The next phase will focus on:

- completing and reviewing representative multiclass annotations
- preparing CT images and labels in nnU-Net format
- training and evaluating the multiclass segmentation model

## Related Work

The [nnUNet4SoilXrayCT repository](https://github.com/MaxPhal/nnUNet4SoilXrayCT)
provides an example of using nnU-Net for soil X-ray CT segmentation and will be
used as a reference during this project.

The goal here is not to completely reproduce that work, but to apply and
evaluate the workflow using the current dataset with a different set of
segmentation classes.