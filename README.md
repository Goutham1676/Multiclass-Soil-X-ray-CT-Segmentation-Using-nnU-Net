# Multiclass Soil X-ray CT Segmentation Using nnU-Net

This project focuses on multiclass segmentation of soil X-ray CT images using
nnU-Net. The classes of interest are soil matrix, stones, organic matter,
roots, biopores, and other pores.

The goal is to build a workflow that starts with manual annotation of ground
truth labels and continues through nnU-Net training, prediction, and evaluation.

## Project Workflow

The planned workflow is:

CT images → annotation in Napari → manual annotation review →
nnU-Net data preparation → preprocessing → training → prediction → evaluation

Napari will be used to create the ground truth annotations. These annotations
will be manually reviewed before they are used for training.

nnU-Net will be used for multiclass segmentation, and the segmentation results
will mainly be evaluated using Dice scores for each class.

## Repository Structure

- `paper/` – project proposal and later manuscript files
- `soilct_segmentation/` – Python code for the project
- `guides/` – supporting documentation from the course template
- `.github/` – GitHub Actions workflows
- `environment.yml` – software environment information
- `pyproject.toml` – Python project configuration

## Setup

The project environment is defined in `environment.yml`.

Create the Conda environment from the repository root:

`conda env create -f environment.yml`

Activate the environment:

`conda activate soilct`

Then start JupyterLab:

`jupyter lab`

## Testing and Validation
Before running pytest, make sure the soilct environment is activated. Run these commands from the repository root:

`conda activate soilct`

Run the tests:

`python -m pytest`

- **test_imports.py** checks that the required libraries can be imported.

- **test_pytest.py** tests core annotation functions and selected invalid inputs.

Expected result: 11 tests passed.

The annotation workflow was manually checked using the input CT stack. Edits made in Napari were saved and remained present after closing and reopening the workflow.

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